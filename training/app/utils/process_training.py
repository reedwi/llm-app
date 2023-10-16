from app.core.celery_app import celery_app
from app.models.supa import SupaChatbotTrainingHook, SupaPersonalChatbotHook
from app.core.logger import get_logger
from supabase import create_client, client
import app.utils.supa as supa
import app.utils.mndy as mndy
import os
import app.utils.pine as pine
import app.utils.lang as lang
import json
from pathlib import Path
import time

logger = get_logger('process_training')
supabase: client = create_client(os.getenv('SUPABASE_URL'), os.getenv('SUPABASE_KEY'))

# @celery_app.task
# def process_training_request(event_body):
#     print(event_body)
#     pass

@celery_app.task
def do_something():
    time.sleep(10)
    logger.info('After 10 seconds')
    return

@celery_app.task
def personal_process_training_request(supa_webhook: dict):
    supa_webhook = SupaPersonalChatbotHook(**supa_webhook)
    logger.info(f'PERSONAL_PROCESS_TRAINING: Entering... : {supa_webhook.record["slack_user_id"]}')
    account = supa.get_one_by_id(supabase=supabase, table_name='accounts', id=supa_webhook.record["account_id"])
    if not account:
        logger.error(f'PERSONAL_PROCESS_TRAINING: ERROR : Could not get account : {supa_webhook.record["account_id"]}')
    logger.info(f'PERSONAL_PROCESS_TRAINING: Account:{account["id"]} ')

    thread_ts_ns = supa_webhook.record["thread_ts"].replace('.', '')
    chatbot_namespace = f'{supa_webhook.record["slack_user_id"]}_{thread_ts_ns}'

    documents = supa.get_by_dynamic_col(supabase=supabase, table_name='documents', column_name='personal_chatbot_id', column_value=supa_webhook.record['id'])
    documents_chunked = []
    logger.info(f'PERSONAL_PROCESS_TRAINING: Entering document loop : {supa_webhook.record["account_id"]}')
    message = ''
    for document in documents:
        
        # Will be an async/background process
        processed_document = process_personal_document(document=document, namespace=chatbot_namespace)

        if processed_document['chunks']:
            documents_chunked.extend(processed_document['chunks'])
            message += f'Successfully added document: {document["document_name"]}\n'
        else:
            logger.error(f'PERSONAL_PROCESS_TRAINING: Processed Document was empty for document: {document} : {supa_webhook.record["account_id"]}')
    logger.info(f'PERSONAL_PROCESS_TRAINING: Finished processing documents, attempting to update pinecone index : {supa_webhook.record["account_id"]}')

    if documents_chunked:
        logger.info(f'PERSONAL_PROCESS_TRAINING: Documents chunked and/or deleted : {supa_webhook.record["account_id"]}')
        if documents_chunked:
            logger.info(f'PERSONAL_PROCESS_TRAINING: Documents chunked : {supa_webhook.record["account_id"]}')
            lang.create_pinecone_index(documents=documents_chunked, namespace=chatbot_namespace)
            logger.info(f'PERSONAL_PROCESS_TRAINING: After pinecone update : {supa_webhook.record["account_id"]}')
        update_chatbot = supa.update_by_id(supabase=supabase, table_name='personal_chatbots', id=supa_webhook.record['id'], data={'status': 'COMPLETE', 'index_internal_name': chatbot_namespace})
    else:
        update_chatbot = supa.update_by_id(supabase=supabase, table_name='personal_chatbots', id=supa_webhook.record['id'], data={'status': 'ERROR'})
    # TODO: For line above need to update the slack portion so that it only looks for chatbots with status of COMPLETE
    # uvicorn workers for the app itself, Pool of celery workers to handle the actual jobs with limited number of workers that can spawn
    # 2 threads/core

@celery_app.task
def process_training_request(supa_webhook: dict):
    supa_webhook = SupaChatbotTrainingHook(**supa_webhook)
    logger.info(f'PROCESS_TRAINING: Entering... : {supa_webhook.record["monday_account_id"]}')
    account = supa.get_account(supabase=supabase, monday_account_id=supa_webhook.record['monday_account_id'])
    if not account:
        logger.error(f'PROCESS_TRAINING: ERROR : Could not get account : {supa_webhook.record["monday_account_id"]}')
    logger.info(f'PROCESS_TRAINING: Account:{account["id"]} : {supa_webhook.record["monday_account_id"]}')

    access_token = supa.get_account_token(supabase=supabase, account_id=account['id'])
    if not access_token:
        logger.error(f'PROCESS_TRAINING: ERROR : Could not get access token : {supa_webhook.record["monday_account_id"]}')
    access_token = access_token['decrypted_monday_access_token']

    chatbot = supa.get_one_by_id(supabase=supabase, table_name='chatbots', id=supa_webhook.record['chatbot_id'])
    if not chatbot:
        logger.error(f'PROCESS_TRAINING: Could not get chatbot {supa_webhook.record["chatbot_id"]} : {supa_webhook.record["monday_account_id"]}')
    if chatbot['index_internal_name']:
        chatbot_namespace = chatbot['index_internal_name']
        chatbot_data = {"status": "BUILDING"}
    else:
        chatbot_namespace = f"{account['id']}_{''.join(c if c.isalnum() else '_' for c in chatbot['name'])}"
        chatbot_data = {"status": "BUILDING", "index_internal_name": chatbot_namespace}
    
    chat_training_item = mndy.create_item_no_values(access_token=access_token, board_id=account['monday_training_board_id'], item_name=f'{chatbot["name"]}')
    try:
        chat_training_id = chat_training_item['data']['create_item']['id']
        logger.info(f'PROCESS_TRAINING: Successfully created chat training item : {supa_webhook.record["monday_account_id"]}')
    except:
        chat_training_id = None
        logger.error(f'PROCESS_TRAINING: ERROR : Could not create chatbot training item : {supa_webhook.record["monday_account_id"]}')
    
    supa.update_by_id(supabase=supabase, table_name='chatbot_trainings', id=supa_webhook.record['id'], data={"monday_board_id": account['monday_training_board_id'], "monday_item_id": chat_training_id})
    supa.update_by_id(supabase=supabase, table_name='chatbots', id=supa_webhook.record['chatbot_id'], data=chatbot_data)

    documents = supa.get_by_dynamic_col(supabase=supabase, table_name='documents', column_name='chatbot_id', column_value=chatbot['id'])
    documents_chunked = []
    deleted_docs = 0
    logger.info(f'PROCESS_TRAINING: Entering document loop : {supa_webhook.record["monday_account_id"]}')
    message = ''
    for document in documents:
        
        # Will be an async/background process
        processed_document = process_document(document=document, namespace=chatbot_namespace, access_token=access_token, document_board=account['monday_documents_board_id'])

        if processed_document['chunks']:
            documents_chunked.extend(processed_document['chunks'])
            message += f'Successfully added document: {document["document_name"]}\n'
        elif processed_document['deleted']:
            deleted_docs += 1
            message += f'Successfully deleted document: {document["document_name"]}\n'
        else:
            logger.error(f'PROCESS_TRAINING: Processed Document was empty for document: {document} : {supa_webhook.record["monday_account_id"]}')
    logger.info(f'PROCESS_TRAINING: Finished processing documents, attempting to update pinecone index : {supa_webhook.record["monday_account_id"]}')

    if documents_chunked or deleted_docs > 0:
        logger.info(f'PROCESS_TRAINING: Documents chunked and/or deleted : {supa_webhook.record["monday_account_id"]}')
        if documents_chunked:
            logger.info(f'PROCESS_TRAINING: Documents chunked : {supa_webhook.record["monday_account_id"]}')
            lang.create_pinecone_index(documents=documents_chunked, namespace=chatbot_namespace)
            logger.info(f'PROCESS_TRAINING: After pinecone update : {supa_webhook.record["monday_account_id"]}')
        update_chatbot = supa.update_by_id(supabase=supabase, table_name='chatbots', id=chatbot['id'], data={'status': 'COMPLETE'})
        update_training = supa.update_by_id(supabase=supabase, table_name='chatbot_trainings', id=supa_webhook.record['id'], data={'status': 'COMPLETE'})
        update_training_board = mndy.update_item(access_token=access_token, board_id=account['monday_training_board_id'], item_id=chat_training_id, column_values=json.dumps(json.dumps({'status': 'Completed', 'long_text': message})))
        update_chatbot_board = mndy.update_item(access_token=access_token, board_id=account['monday_chatbots_board_id'], item_id=chatbot['item_id'], column_values=json.dumps(json.dumps({'status': 'Completed', 'long_text': ''})))
    else:
        update_chatbot = supa.update_by_id(supabase=supabase, table_name='chatbots', id=chatbot['id'], data={'status': 'ERROR'})
        update_training = supa.update_by_id(supabase=supabase, table_name='chatbot_trainings', id=supa_webhook.record['id'], data={'status': 'ERROR'})
        update_training_board = mndy.update_item(access_token=access_token, board_id=account['monday_training_board_id'], item_id=chat_training_id, column_values=json.dumps(json.dumps({'status': 'ERROR', 'long_text': 'Please check documents table for potential issues with this training'})))
        update_chatbot_board = mndy.update_item(access_token=access_token, board_id=account['monday_chatbots_board_id'], item_id=chatbot['item_id'], column_values=json.dumps(json.dumps({'status': 'ERROR', 'long_text': 'Please check documents table for potential issues with this training'})))
    # TODO: For line above need to update the slack portion so that it only looks for chatbots with status of COMPLETE
    # uvicorn workers for the app itself, Pool of celery workers to handle the actual jobs with limited number of workers that can spawn
    # 2 threads/core


def delete_document(document: dict, namespace: str, in_index: bool, access_token: str, documents_board_id: int):
    if in_index:
        pine.delete_vectors(namespace=namespace, document_id=document['document_object'])
    try:
        document_storage_obj = supa.get_object_row(supabase=supabase, document_id=document['document_object'])
        mndy.update_item(access_token=access_token, board_id=documents_board_id, item_id=document['item_id'], column_values=json.dumps(json.dumps({'status': 'In Model'})))
        supa.delete_bucket_object(supabase=supabase, bucket_name=document['bucket_location'], path=document_storage_obj['name'])
        supa.delete_by_id(supabase=supabase, table_name='documents', id=document['id'])
        return True
    except:
        logger.error(f'DELETE_DOCUMENT: ERROR : Could not delete {document} from program')
        return

def insert_document(document: dict, namespace: str, access_token: str, documents_board_id: int):
    obj = supa.get_object_row(supabase=supabase, document_id=document['document_object'])
    file_name = obj['path_tokens'][-1]
    file_content = supa.get_file(supabase=supabase, bucket_id=document['bucket_location'], folder_path=obj['name'])

    save_path = Path(f'./data_folder/{document["monday_account_id"]}/{namespace}/{file_name}')
    save_path.parent.mkdir(parents=True, exist_ok=True)

    with save_path.open(mode='wb') as file:
        file.write(file_content)

    chunks = []
    invalid = False
    match save_path.suffix.lower():
        case '.txt':
            chunks = lang.load_and_split_txt(file_path=str(save_path.resolve()), namespace=namespace, file_name=file_name, doc_id=document['document_object']) 
        case '.pdf':
            chunks = lang.load_and_split_pdf(file_path=str(save_path.resolve()), namespace=namespace, file_name=file_name, doc_id=document['document_object'])
        case '.doc':
            chunks = lang.load_and_split_doc(file_path=str(save_path.resolve()), namespace=namespace, file_name=file_name, doc_id=document['document_object']) 
        case '.docx':
            chunks = lang.load_and_split_doc(file_path=str(save_path.resolve()), namespace=namespace, file_name=file_name, doc_id=document['document_object'])
        case '.csv':
            chunks = lang.load_and_split_csv(file_path=str(save_path.resolve()), namespace=namespace, file_name=file_name, doc_id=document['document_object'])
        case '.xls':
            chunks = lang.load_and_split_excel(file_path=str(save_path.resolve()), namespace=namespace, file_name=file_name, doc_id=document['document_object'])
        case '.xlsx':
            chunks = lang.load_and_split_excel(file_path=str(save_path.resolve()), namespace=namespace, file_name=file_name, doc_id=document['document_object'])
        case _:
            mndy.send_document_error(access_token=access_token, board_id=documents_board_id, item_id=document['item_id'], message=f'Unsupported document type for file: {file_name}')
            delete_document(document=document, namespace=namespace, in_index=False, access_token=access_token, documents_board_id=documents_board_id)
            invalid = True
    if chunks:
        mndy.update_item(access_token=access_token, board_id=documents_board_id, item_id=document['item_id'], column_values=json.dumps(json.dumps({'status': 'In Model', 'long_text': ''})))
        supa.update_by_id(supabase=supabase, table_name='documents', id=document['id'], data={'file_status': 'COMPLETE'})
    save_path.unlink(missing_ok=True)
    return chunks, invalid

def process_document(document: dict, namespace: str, access_token: str, document_board: int):
    logger.info(f'PROCESS_DOCUMENT: Entering for document: {document}')
    processed_document = {'chunks': None, 'deleted': False}
    if document['file_status'] == 'DELETE':
        logger.info('PROCESS_DOCUMENT: Deleting document')
        deleted = delete_document(document=document, namespace=namespace, in_index=True, access_token=access_token, documents_board_id=document_board)
        processed_document['chunks'] = None
        processed_document['deleted'] = True

    elif document['file_status'] == 'INSERT':
        logger.info('PROCESS_DOCUMENT: Chunking document')
        document_chunks, invalid_format = insert_document(document=document, namespace=namespace, access_token=access_token, documents_board_id=document_board)
        if document_chunks:
            processed_document['chunks'] = document_chunks
            processed_document['deleted'] = False
        elif not invalid_format:
            mndy.update_item(access_token=access_token, board_id=document_board, item_id=document['item_id'], column_values=json.dumps(json.dumps({'status': 'ERROR', 'long_text': 'Error processing this document. Please make sure the document uploaded has data'})))
            logger.error(f'PROCESS_DOCUMENT: ERROR : Potential issue chunking document: {document_chunks}')
    else:
        logger.info(f'PROCESS_DOCUMENT: Document is not in INSERT or DELETE status')
        processed_document['chunks'] = None
        processed_document['deleted'] = False
    return processed_document



def insert_personal_document(document: dict, namespace: str):
    obj = supa.get_object_row(supabase=supabase, document_id=document['document_object'])
    file_name = obj['path_tokens'][-1]
    file_content = supa.get_file(supabase=supabase, bucket_id=document['bucket_location'], folder_path=obj['name'])

    save_path = Path(f'./data_folder/{document["account_id"]}/{namespace}/{file_name}')
    save_path.parent.mkdir(parents=True, exist_ok=True)

    with save_path.open(mode='wb') as file:
        file.write(file_content)

    chunks = []
    invalid = False
    match save_path.suffix.lower():
        case '.txt':
            chunks = lang.load_and_split_txt(file_path=str(save_path.resolve()), namespace=namespace, file_name=file_name, doc_id=document['document_object']) 
        case '.pdf':
            chunks = lang.load_and_split_pdf(file_path=str(save_path.resolve()), namespace=namespace, file_name=file_name, doc_id=document['document_object'])
        case '.doc':
            chunks = lang.load_and_split_doc(file_path=str(save_path.resolve()), namespace=namespace, file_name=file_name, doc_id=document['document_object']) 
        case '.docx':
            chunks = lang.load_and_split_doc(file_path=str(save_path.resolve()), namespace=namespace, file_name=file_name, doc_id=document['document_object'])
        case '.csv':
            chunks = lang.load_and_split_csv(file_path=str(save_path.resolve()), namespace=namespace, file_name=file_name, doc_id=document['document_object'])
        case '.xls':
            chunks = lang.load_and_split_excel(file_path=str(save_path.resolve()), namespace=namespace, file_name=file_name, doc_id=document['document_object'])
        case '.xlsx':
            chunks = lang.load_and_split_excel(file_path=str(save_path.resolve()), namespace=namespace, file_name=file_name, doc_id=document['document_object'])
    if chunks:
        supa.update_by_id(supabase=supabase, table_name='documents', id=document['id'], data={'file_status': 'COMPLETE'})
    save_path.unlink(missing_ok=True)
    return chunks, invalid

def process_personal_document(document: dict, namespace: str):
    logger.info(f'PERSONAL_PROCESS_DOCUMENT: Entering for document: {document}')
    processed_document = {'chunks': None}
    if document['file_status'] == 'INSERT':
        logger.info('PERSONAL_PROCESS_DOCUMENT: Chunking document')
        document_chunks, invalid_format = insert_personal_document(document=document, namespace=namespace)
        if document_chunks:
            processed_document['chunks'] = document_chunks
            processed_document['deleted'] = False
        elif not invalid_format:
            logger.error(f'PERSONAL_PROCESS_DOCUMENT: ERROR : Potential issue chunking document: {document_chunks}')
    else:
        logger.info(f'PERSONAL_PROCESS_DOCUMENT: Document is not in INSERT or DELETE status')
        processed_document['chunks'] = None
        processed_document['deleted'] = False
    return processed_document


####################################################################################
####################################################################################
####################################################################################
####################################################################################
####################################################################################
###################         DEV   ##################################################
####################################################################################
####################################################################################
####################################################################################

@celery_app.task
def personal_process_training_request_dev(supa_webhook: dict):
    supa_webhook = SupaPersonalChatbotHook(**supa_webhook)
    logger.info(f'PERSONAL_PROCESS_TRAINING: Entering... : {supa_webhook.record["slack_user_id"]}')
    account = supa.get_one_by_id(supabase=supabase, table_name='dev_accounts', id=supa_webhook.record["account_id"])
    if not account:
        logger.error(f'PERSONAL_PROCESS_TRAINING: ERROR : Could not get account : {supa_webhook.record["account_id"]}')
    logger.info(f'PERSONAL_PROCESS_TRAINING: Account:{account["id"]} ')

    thread_ts_ns = supa_webhook.record["thread_ts"].replace('.', '')
    chatbot_namespace = f'{supa_webhook.record["slack_user_id"]}_{thread_ts_ns}'

    documents = supa.get_by_dynamic_col(supabase=supabase, table_name='dev_documents', column_name='personal_chatbot_id', column_value=supa_webhook.record['id'])
    documents_chunked = []
    logger.info(f'PERSONAL_PROCESS_TRAINING: Entering document loop : {supa_webhook.record["account_id"]}')
    message = ''
    for document in documents:
        
        # Will be an async/background process
        processed_document = process_personal_document_dev(document=document, namespace=chatbot_namespace)

        if processed_document['chunks']:
            documents_chunked.extend(processed_document['chunks'])
            message += f'Successfully added document: {document["document_name"]}\n'
        else:
            logger.error(f'PERSONAL_PROCESS_TRAINING: Processed Document was empty for document: {document} : {supa_webhook.record["account_id"]}')
    logger.info(f'PERSONAL_PROCESS_TRAINING: Finished processing documents, attempting to update pinecone index : {supa_webhook.record["account_id"]}')

    if documents_chunked:
        logger.info(f'PERSONAL_PROCESS_TRAINING: Documents chunked and/or deleted : {supa_webhook.record["account_id"]}')
        if documents_chunked:
            logger.info(f'PERSONAL_PROCESS_TRAINING: Documents chunked : {supa_webhook.record["account_id"]}')
            lang.create_pinecone_index(documents=documents_chunked, namespace=chatbot_namespace)
            logger.info(f'PERSONAL_PROCESS_TRAINING: After pinecone update : {supa_webhook.record["account_id"]}')
        update_chatbot = supa.update_by_id(supabase=supabase, table_name='dev_personal_chatbots', id=supa_webhook.record['id'], data={'status': 'COMPLETE', 'index_internal_name': chatbot_namespace})
    else:
        update_chatbot = supa.update_by_id(supabase=supabase, table_name='dev_personal_chatbots', id=supa_webhook.record['id'], data={'status': 'ERROR'})

def insert_personal_document_dev(document: dict, namespace: str):
    obj = supa.get_object_row(supabase=supabase, document_id=document['document_object'])
    file_name = obj['path_tokens'][-1]
    file_content = supa.get_file(supabase=supabase, bucket_id=document['bucket_location'], folder_path=obj['name'])

    save_path = Path(f'./data_folder/{document["account_id"]}/{namespace}/{file_name}')
    save_path.parent.mkdir(parents=True, exist_ok=True)

    with save_path.open(mode='wb') as file:
        file.write(file_content)

    chunks = []
    invalid = False
    match save_path.suffix.lower():
        case '.txt':
            chunks = lang.load_and_split_txt(file_path=str(save_path.resolve()), namespace=namespace, file_name=file_name, doc_id=document['document_object']) 
        case '.pdf':
            chunks = lang.load_and_split_pdf(file_path=str(save_path.resolve()), namespace=namespace, file_name=file_name, doc_id=document['document_object'])
        case '.doc':
            chunks = lang.load_and_split_doc(file_path=str(save_path.resolve()), namespace=namespace, file_name=file_name, doc_id=document['document_object']) 
        case '.docx':
            chunks = lang.load_and_split_doc(file_path=str(save_path.resolve()), namespace=namespace, file_name=file_name, doc_id=document['document_object'])
        case '.csv':
            chunks = lang.load_and_split_csv(file_path=str(save_path.resolve()), namespace=namespace, file_name=file_name, doc_id=document['document_object'])
        case '.xls':
            chunks = lang.load_and_split_excel(file_path=str(save_path.resolve()), namespace=namespace, file_name=file_name, doc_id=document['document_object'])
        case '.xlsx':
            chunks = lang.load_and_split_excel(file_path=str(save_path.resolve()), namespace=namespace, file_name=file_name, doc_id=document['document_object'])
    if chunks:
        supa.update_by_id(supabase=supabase, table_name='dev_documents', id=document['id'], data={'file_status': 'COMPLETE'})
    save_path.unlink(missing_ok=True)
    return chunks, invalid

def process_personal_document_dev(document: dict, namespace: str):
    logger.info(f'PERSONAL_PROCESS_DOCUMENT: Entering for document: {document}')
    processed_document = {'chunks': None}
    if document['file_status'] == 'INSERT':
        logger.info('PERSONAL_PROCESS_DOCUMENT: Chunking document')
        document_chunks, invalid_format = insert_personal_document_dev(document=document, namespace=namespace)
        if document_chunks:
            processed_document['chunks'] = document_chunks
            processed_document['deleted'] = False
        elif not invalid_format:
            logger.error(f'PERSONAL_PROCESS_DOCUMENT: ERROR : Potential issue chunking document: {document_chunks}')
    else:
        logger.info(f'PERSONAL_PROCESS_DOCUMENT: Document is not in INSERT or DELETE status')
        processed_document['chunks'] = None
        processed_document['deleted'] = False
    return processed_document