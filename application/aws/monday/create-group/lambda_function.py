import json
import requests
import jwt
import os
from supabase import create_client, Client
import lib.supa as supa
import json
import lib.mndy as mndy
import logging

SIGNING_SECRET = os.getenv('MONDAY_SIGNING_SECRET')
supabase: Client = create_client(os.getenv('SUPABASE_URL'), os.getenv('SUPABASE_KEY'))
logger = logging.getLogger()
logger.setLevel(logging.INFO) 

def lambda_handler(event, context):
    logger.info('[MNDY_CREATE_GROUP]: ENTER')
    auth_token = event['headers']['authorization']
    event['body'] = json.loads(event['body'])
    item_id = event['body']['payload']['inputFields']['itemId']
    board_id = event['body']['payload']['inputFields']['boardId']

    decoded_header = jwt.decode(jwt=auth_token, key=os.getenv('MONDAY_SIGNING_SECRET'), algorithms=['HS256'], audience="https://tierrybqzqrfo4madpdokfyygy0leaeb.lambda-url.us-east-1.on.aws/")
    logger.info(f'[MNDY_CREATE_GROUP]: START : {decoded_header["accountId"]}')
    
    account = supa.get_account(supabase=supabase, monday_account_id=decoded_header['accountId'])
    if not account:
        logger.error(f'[MNDY_CREATE_GROUP]: ERROR : Cannot find a corresponding account in the account table for mndy account: {decoded_header["accountId"]}')
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

    account_access = supa.get_account_token(supabase=supabase, account_id=account['id'])
    if not account_access:
        logger.error(f'[MNDY_CREATE_GROUP]: ERROR : Cannot find a corresponding account token the account table for mndy account: {decoded_header["accountId"]}')
        return return_success()
    
    current_chatbots = supa.get_chatbots(supabase=supabase, account_id=account['id'])
    current_chatbot_names = [str.lower(chatbot['name']).strip() for chatbot in current_chatbots]

    item = mndy.get_item(access_token=account_access['decrypted_monday_access_token'], item_id=item_id)
    try:
        item_name = item['data']['items'][0]['name'].strip()
    except:
        logger.error(f'[MNDY_CREATE_GROUP]: ERROR : Issue getting item name for item_id: {item_id}\nItem Details: {item}')
        return return_success()
    
    if str.lower(item_name) in current_chatbot_names:
        # There is possibly a duplicate chatbot name do something
        pass
    

    groups = mndy.get_groups_from_board(access_token=account_access['decrypted_monday_access_token'], board_id=account['monday_documents_board_id'])
    try:
        group_names = [str.lower(group['title']).strip() for group in groups['data']['boards'][0]['groups']]
        if str.lower(item_name) in group_names:
            # Means there is already a group with this item name and do something
            mndy.delete_item(access_token=account_access['decrypted_monday_access_token'], item_id=item_id)
            return return_success()
    except:
        logger.info(f'[MNDY_CREATE_GROUP]: No groups to process currenlty : {groups} : {decoded_header["accountId"]}')
    
    chatbot_group_id = mndy.create_group_in_board(access_token=account_access['decrypted_monday_access_token'], board_id=account['monday_documents_board_id'], group_name=item_name)
    logger.info(f'[MNDY_CREATE_GROUP]: Document Group, {item_name}, created in documents board for {decoded_header["accountId"]}')

    supa.create_chatbot_row(
        supabase=supabase,
        account_id=account['id'],
        item_id=item_id,
        board_id=board_id,
        name=item_name,
        group_id=chatbot_group_id,
        documents_board_id=account['monday_documents_board_id']
    )
    logger.info(f'[MNDY_CREATE_GROUP]: END : {decoded_header["accountId"]}')
    return return_success()

def return_success():
    return {
        'statusCode': 200,
        'body': json.dumps('Hello from Lambda!')
    }