from typing import Any
from app.core.logger import get_logger
logger = get_logger('supabase')

def get_account(supabase, monday_account_id):
    supabase.postgrest.schema('public')
    item = supabase.table('accounts').select('*').eq('monday_account_id', monday_account_id).execute()

    try:
        account = item.data[0]
    except:
        account = None
        print('Could not return account from supabase')
    return account

def get_account_token(supabase, account_id):
    supabase.postgrest.schema('public')
    item = supabase.table('decrypted_accounts').select('decrypted_monday_access_token').eq('id', account_id).execute()

    try:
        account_access = item.data[0]
    except:
        account_access = None
        print('Could not return account access from supabase')
    return account_access


def create_chatbot_row(supabase, account_id, item_id, board_id, name, group_id, documents_board_id):
    supabase.postgrest.schema('public')
    chatbot = {
        'chatbots_board_id': board_id,
        'account_id': account_id,
        'item_id': item_id,
        'name': name,
        'group_name': name,
        'group_internal_name': group_id,
        'documents_board_id': documents_board_id
    }
    supabase.table('chatbots').insert(chatbot).execute()

def get_chatbots(supabase, account_id):
    supabase.postgrest.schema('public')
    item = supabase.table('chatbots').select('*').eq('account_id', account_id).execute()

    try:
        chatbots = item.data
    except:
        chatbots = None
        print('Could not return chatbots from supabase')
    return chatbots


def get_chatbot_row(supabase, item_id):
    supabase.postgrest.schema('public')
    item = supabase.table('chatbots').select('*').eq('item_id', item_id).execute()

    try:
        chatbot = item.data[0]
    except:
        chatbot = None
        print('Could not return account from supabase')
    return chatbot


def update_chatbot_row(supabase, row_id, name):
    supabase.postgrest.schema('public')
    data = {
        'group_name': name,
        'name': name
    }
    item = supabase.table('chatbots').update(data).eq('id', row_id).execute()
    try:
        return item.data
    except:
        print('Could not update data in supabase')
        return None

def get_one_by_id(supabase, table_name: str, id: int) -> dict:
    supabase.postgrest.schema('public')
    item = supabase.table(table_name).select('*').eq('id', id).execute()
    try:
        return item.data[0]
    except:
        print('Could not return one row from supabase')
        return None


def get_by_dynamic_col(supabase, table_name: str, column_name: str, column_value: Any) -> list[dict]:
    supabase.postgrest.schema('public')
    items = supabase.table(table_name).select('*').eq(column_name, column_value).execute()
    try:
        return items.data
    except:
        print('Could not return one row from supabase')
        return None
    

def get_all(supabase, table_name: str) -> list[dict]:
    supabase.postgrest.schema('public')
    items = supabase.table(table_name).select('*').execute()
    try:
        return items.data
    except:
        print('Could not get all rows from supabase')
        return None
    

def insert(supabase, table_name: str, data: dict) -> dict | list[dict]:
    supabase.postgrest.schema('public')
    item = supabase.table(table_name).insert(data).execute()
    try:
        return item.data
    except:
        print('Could not insert data into supabase')
        return None
    


def update_by_id(supabase, table_name: str, id: int, data: dict) -> list[dict]:
    supabase.postgrest.schema('public')
    item = supabase.table(table_name).update(data).eq('id', id).execute()
    try:
        return item.data
    except:
        print('Could not update data in supabase')
        return None


def update_by_dynamic_col(supabase, table_name: str, column_name: str, column_value:Any, data: dict) -> list[dict]:
    supabase.postgrest.schema('public')
    item = supabase.table(table_name).update(data).eq(column_name, column_value).execute()
    try:
        return item.data
    except:
        print('Could not update data in supabase')
        return None
    

def delete_by_id(supabase, table_name: str, id: int) -> None:
    supabase.postgrest.schema('public')
    item = supabase.table(table_name).delete().eq('id', id).execute()
    return


def delete_by_dynamic_col(supabase, table_name:str, column_name: str, column_value: Any) -> None:
    supabase.postgrest.schema('public')
    item = supabase.table(table_name).delete().eq(column_name, column_value).execute()
    return


def get_object_row(supabase, document_id: str) -> dict:
    object_row = supabase.postgrest.schema('storage').table('objects').select('*').eq('id', document_id).execute()
    try:
        return object_row.data[0]
    except:
        print('Error getting value')

def get_object_row_by_name_and_bucket(supabase, bucket_id: str, path: str) -> dict:
    object_row = supabase.postgrest.schema('storage').table('objects').select('*').eq('bucket_id', bucket_id).eq('name', path).execute()
    try:
        return object_row.data[0]
    except:
        print('Error getting value')


def get_file(supabase, bucket_id: Any, folder_path: str):
    file = supabase.storage.from_(id=bucket_id).download(path=folder_path)
    return file


def get_file_url(supabase, bucket_id: Any, folder_path: str):
    file = supabase.storage.from_(bucket_id).get_public_url(path=folder_path)
    return file


def create_bucket(supabase, bucket_name: str):
    bucket = supabase.storage.create_bucket(id=bucket_name)
    return bucket

def get_bucket(supabase, bucket_name: str):
    try:
        bucket = supabase.storage.get_bucket(id=bucket_name)
        return bucket
    except:
        print(f'Bucket: {bucket_name} does not exist')
        return None

def get_bucket_folders(supabase, bucket_name: str):
    folders = supabase.storage.get_bucket(id=bucket_name).list()
    return folders


def get_bucket_objects(supabase, bucket_name: str, folder: str):
    try:
        objects = supabase.storage.get_bucket(id=bucket_name).list(folder)
        return objects
    except:
        print('Bucket folder does not exist')
        return None
    
def create_bucket_object(supabase, bucket_name: str, path: str, file_contents):
    file_return = supabase.storage.get_bucket(id=bucket_name).upload(path=path, file=file_contents)
    return file_return


def update_bucket_object(supabase, bucket_name: str, path: str, file_contents):
    try:
        supabase.storage.get_bucket(id=bucket_name).remove(paths=[path])
        file_return = supabase.storage.get_bucket(id=bucket_name).upload(path=path, file=file_contents)
        return file_return
    except:
        print('Error updating bucket object')


def delete_bucket_object(supabase, bucket_name: str, path: str):
    try:
        supabase.storage.get_bucket(id=bucket_name).remove(paths=[path])
    except:
        print('Error deleting bucket object')