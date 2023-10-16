from index_config import logger
import index_config.supabase_obo as supa
import index_config.langchain_obo as lang
import index_config.monday_obo as mf
import index_config.helpers_obo as help
from pathlib import Path
from pprint import pprint
import requests



def extract_monday(monday_account_id: str):
    '''
    Gets the item values and files from a specific monday board and returns a list of "documents"
    '''
    account = supa.get_by_dynamic_col(
        table_name='accounts',
        column_name='monday_account_id',
        column_value=monday_account_id
    )
    try:
        account = account[0]
    except:
        logger.error('Could not get account from account table via Monday Id')
        return
    
    item_ids = mf.get_item_ids(board_id=account['monday_board_id'], api_key=account['monday_api_key'])
    item_values = mf.get_item_values(item_ids=item_ids, api_key=account['monday_api_key'])
    parsed_documents = mf.process_item_values(item_values=item_values, monday_account_id=monday_account_id)
    return parsed_documents


def process_documents(documents: list[dict], monday_account_id: str):
    '''
    Takes the list of documents from the extracted monday boards and processes them
    First it looks to create bucket for the monday account if it doesn't exist
    Then we loop through each document
    1. Look to see if this a document that already exists in the database
        a. If it is and it is set to "Remove", we delete the object from the bucket
        b. If it is not set to remove, then we update the existing object in the bucket and update the document row
    2. If the document is new then
        a. Insert a new object in the bucket
        b. Insert a new row in the documents table
    '''
    account = supa.get_by_dynamic_col(
        table_name='accounts',
        column_name='monday_account_id',
        column_value=monday_account_id
    )
    try:
        account = account[0]
    except:
        logger.error('Could not get account from account table via Monday Id')
        return
    # Get current bucket folders
    bucket = supa.get_bucket(bucket_name=monday_account_id)
    if not bucket:
        bucket = supa.create_bucket(bucket_name=monday_account_id)

    for document in documents:
        document_row = supa.get_by_dynamic_col(table_name='documents', column_name='item_id', column_value=document['item_id'])
        if document_row:
            document_row = document_row[0]
            supa_file_path = f'{document["group_name"]}/{document["file_name"]}'
            local_file_path = f'./data_folder/tmp/{document["file_name"]}'
            
            if document['file_status'] == 'Remove':
                supa.delete_bucket_object(bucket_name=monday_account_id, path=supa_file_path)
                # TODO: Do I delete the row from the documents table as well. I think not
            else:
                local_file_object = help.download_file(
                    url=document['public_monday_url'],
                    local_filename=local_file_path
                )

                supa_file_object = supa.update_bucket_object(
                    bucket_name=monday_account_id, 
                    path=supa_file_path,
                    file_contents=local_file_object
                )
                help.delete_local_file(local_file_path)
                supa_storage_row = supa.get_object_row_by_name_and_bucket(
                    bucket_id=monday_account_id,
                    path=supa_file_path
                )
                document_row['public_monday_url'] = document['public_monday_url']
                document_row['document_object'] = supa_storage_row['id']
                supa.update_by_id(table_name='documents', id=document_row['id'], data=document_row)

        else:
            supa_file_path = f'{document["group_name"]}/{document["file_name"]}'
            local_file_path = f'./data_folder/tmp/{document["file_name"]}'

            local_file_object = help.download_file(
                url=document['public_monday_url'],
                local_filename=local_file_path
            )

            supa_file_object = supa.create_bucket_object(
                bucket_name=monday_account_id, 
                path=supa_file_path,
                file_contents=local_file_object
            )

            help.delete_local_file(local_file_path)

            supa_storage_row = supa.get_object_row_by_name_and_bucket(
                bucket_id=monday_account_id,
                path=supa_file_path
            )

            document['bucket_location'] = monday_account_id
            document['document_object'] = supa_storage_row['id']
            document_row = supa.insert(table_name='documents', data=document)



def update_index():
    pass

def create_index(monday_account_id: str):
    logger.info('BEGINNING INDEX CREATION ROUTINE')
    account = supa.get_by_dynamic_col(
        table_name='accounts',
        column_name='monday_account_id',
        column_value=monday_account_id
    )
    try:
        account = account[0]
    except:
        logger.error('Could not get account from account table via Monday Id')
        return
    
    documents = supa.get_by_dynamic_col(
        table_name='documents',
        column_name='monday_account_id',
        column_value=monday_account_id
    )

    account_path = Path(f'./data_folder/{monday_account_id}')
    account_path.mkdir(parents=True, exist_ok=True)

    # TODO: Decide if I want to add to index within loop or create index all at once
    document_chunks = []
    for document in documents:
        obj = supa.get_object_row(document_id=document['document_object'])
        namespace, file_name = obj['path_tokens']
        file_content = supa.get_file(bucket_id=monday_account_id, folder_path=obj['name'])

        save_path = Path(f'./data_folder/{monday_account_id}/{namespace}/{file_name}')
        save_path.parent.mkdir(parents=True, exist_ok=True)

        with save_path.open(mode='wb') as file:
            file.write(file_content)

        chunks = []
        match save_path.suffix:
            case '.txt':
                chunks = lang.load_and_split_txt(file_path=save_path, namespace=namespace, file_url=document['private_monday_url'], file_name=file_name, doc_id=document['document_object'])
            
            case '.pdf':
                chunks = lang.load_and_split_pdf(file_path=save_path, namespace=namespace, file_url=document['private_monday_url'], file_name=file_name, doc_id=document['document_object'])
            
            case '.doc':
                chunks = lang.load_and_split_doc(file_path=save_path, namespace=namespace, file_url=document['private_monday_url'], file_name=file_name, doc_id=document['document_object'])
            
            case '.docx':
                chunks = lang.load_and_split_doc(file_path=save_path, namespace=namespace, file_url=document['private_monday_url'], file_name=file_name, doc_id=document['document_object'])
            
            case '.csv':
                print('csv')
        if chunks:
            document_chunks.extend(chunks)
    
    try:
        vector_db = lang.create_pinecone_index(documents=document_chunks, namespace=monday_account_id)
    except:
        logger.error('Error creating index')
    
    #TODO: Delete all documents locally

if __name__ == '__main__':
    # supa.get_bucket_objects(bucket_name='12345', folder='Namespace 3')
    # exit()
    documents = extract_monday(monday_account_id='12345')
    process_documents(documents=documents, monday_account_id='12345')
    #TODO: Working on process documents to download and upload file
    # create_index(monday_account_id='12345')
    # update_index()
    pass