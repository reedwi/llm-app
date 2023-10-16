import json
import requests
import jwt
import os
import lib.supa as supa
import json
import lib.mndy as mndy
from supabase import client, create_client
import logging

SIGNING_SECRET = os.getenv('MONDAY_SIGNING_SECRET')
supabase: client = create_client(os.getenv('SUPABASE_URL'), os.getenv('SUPABASE_KEY'))
logger = logging.getLogger()
logger.setLevel(logging.INFO)

def lambda_handler(event, context):
    # TODO implement
    logger.info(f'[MNDY_DELETE_CHATBOT]: ENTER')
    auth_token = event['headers']['authorization']
    event['body'] = json.loads(event['body'])
    item_id = event['body']['payload']['inputFields']['itemId']
    board_id = event['body']['payload']['inputFields']['boardId']

    decoded_header = jwt.decode(jwt=auth_token, key=os.getenv('MONDAY_SIGNING_SECRET'), algorithms=['HS256'], audience="https://saqy3j2f7lwqq4o5bvf22aojpm0rvbrg.lambda-url.us-east-1.on.aws/")
    logger.info(f'[MNDY_DELETE_CHATBOT]: START : {decoded_header["accountId"]}')

    account = supa.get_account(supabase=supabase, monday_account_id=decoded_header['accountId'])
    if not account:
        logger.error(f'[MNDY_DELETE_CHATBOT]: ERROR : Cannot find a corresponding account in the account table for mndy account: {decoded_header["accountId"]}')
        return return_success()
    
    if not account['monday_chatbots_board_id']:
        logger.info(f'[MNDY_CREATE_GROUP]: No Board Ids yet for account_id: {decoded_header["accountId"]}')
        supa.update_by_id(supabase=supabase, table_name='accounts', id=account['id'], data={'monday_chatbots_board_id': board_id})
        account['monday_chatbots_board_id'] = board_id

        board_folder_id, workspace_id = mndy.get_board_folder_and_workspace(access_token=decoded_header['shortLivedToken'], board_id=board_id)
        logger.info(f'{board_folder_id}, {workspace_id}')
        if workspace_id or board_folder_id:
            boards = mndy.get_boards_in_workspace(access_token=decoded_header['shortLivedToken'], workspace_id=workspace_id)
            documents_id, usage_id, trainings_id = mndy.get_board_ids_for_account(boards)
            data = {
                'monday_documents_board_id': documents_id,
                'monday_usage_board_id': usage_id,
                'monday_training_board_id': trainings_id
            }
            supa.update_by_id(supabase=supabase, table_name='accounts', id=account['id'], data=data)
            account = supa.get_account(supabase=supabase, monday_account_id=decoded_header['accountId'])
            logger.info(f'[MNDY_CREATE_GROUP]: SUCCESS : Board Ids set for account_id: {decoded_header["accountId"]}')
        else:
            logger.error(f'[MNDY_CREATE_GROUP]: ERROR : getting initial board ids for monday account id: {decoded_header["accountId"]}')

    chatbot_row = supa.get_chatbot_row(supabase=supabase, item_id=item_id)
    if not chatbot_row:
        logger.error(f'[MNDY_DELETE_CHATBOT]: No chatbot row in supabase table for item_id: {item_id} : {decoded_header["accountId"]}')
        data = {
            "status": {
                "label": "ERROR"
            },
            "long_text": {
                "text": "Cannot find corresponding group. Please delete the chatbot item here and group manually in the Documents board."
            }
        }
        update_item = mndy.update_item(access_token=decoded_header['shortLivedToken'], board_id=board_id, item_id=item_id, column_values=json.dumps(json.dumps(data)))
        return return_success()
    
    mndy.delete_group(access_token=decoded_header['shortLivedToken'], board_id=chatbot_row['documents_board_id'], group_id=chatbot_row['group_internal_name'])
    logger.info(f'[MNDY_DELETE_CHATBOT]: DELETED GROUP : {decoded_header["accountId"]}')
    mndy.delete_item(access_token=decoded_header['shortLivedToken'], item_id=item_id)
    logger.info(f'[MNDY_DELETE_CHATBOT]: DELETED CHATBOT ITEM : {decoded_header["accountId"]}')

    supa.empty_bucket_folder(supabase=supabase, bucket_id=account['monday_account_id'], folder=chatbot_row['group_internal_name'])
    logger.info(f'[MNDY_DELETE_CHATBOT]: DELETED SUPABASE BUCKET : {decoded_header["accountId"]}')
    supa.delete_by_id(supabase=supabase, table_name='chatbots', id=chatbot_row['id'])
    logger.info(f'[MNDY_DELETE_CHATBOT]: DELETED CHATBOT ROW IN SUPABASE : {decoded_header["accountId"]}')
    logger.info(f'[MNDY_DELETE_CHATBOT]: END : {decoded_header["accountId"]}')
    return return_success()
    
    
def return_success():
    return {
        'statusCode': 200,
        'body': json.dumps('Hello from Lambda!')
    }