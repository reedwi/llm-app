import json
import jwt
import requests
import os
from supabase import create_client, client
import lib.supa as supa
import json
import lib.mndy as mndy
from lib.types import TrainingDocQueueMsg
import boto3
import logging
import time

sqs_client = boto3.client('sqs')

SIGNING_SECRET = os.getenv('MONDAY_SIGNING_SECRET')
supabase: client = create_client(os.getenv('SUPABASE_URL'), os.getenv('SUPABASE_KEY'))
logger = logging.getLogger()
logger.setLevel(logging.INFO) 

def lambda_handler(event, context):
    logger.info('[MNDY_TRAIN_CHATBOT]: ENTER')
    auth_token = event['headers']['authorization']
    event['body'] = json.loads(event['body'])
    item_id = event['body']['payload']['inputFields']['itemId']
    board_id = event['body']['payload']['inputFields']['boardId']

    decoded_header = jwt.decode(jwt=auth_token, key=os.getenv('MONDAY_SIGNING_SECRET'), algorithms=['HS256'], audience="https://62xiue7nr5hn4v2ele2e47y2jq0gbwgf.lambda-url.us-east-1.on.aws/")
    logger.info(f'[MNDY_TRAIN_CHATBOT]: START : {decoded_header["accountId"]}')
    time.sleep(1)
    item = mndy.get_item(access_token=decoded_header['shortLivedToken'], item_id=item_id)
    custom_no_answer = None
    for column in item['data']['items'][0]['column_values']:
        if column['id'] == 'status':
            if column['text'] == 'Model is Building':
                logger.info(f'[MNDY_TRAIN_CHATBOT]: Chatbot item is already in "Model is Building" status : {decoded_header["accountId"]}')
                return return_success()
        elif column['id'] == 'long_text2':
            if column['text'] not in ['', None]:
                custom_no_answer = column['text']


    account = supa.get_account(supabase=supabase, monday_account_id=decoded_header['accountId'])
    if not account: 
        logger.error(f'[MNDY_TRAIN_CHATBOT]: ERROR : No account found for account_id: {decoded_header["accountId"]}')
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
    if not account: return return_success()
    
    chatbot_row = supa.get_chatbot_row(supabase=supabase, item_id=item_id)
    if not chatbot_row: 
        logger.error(f'[MNDY_TRAIN_CHATBOT]: ERROR : No chatbot row found for item_id: {item_id} : {decoded_header["accountId"]}')
        return return_success()
    elif chatbot_row['no_answer_response'] != custom_no_answer:
        print('in the if')
        supa.update_by_id(supabase=supabase, table_name='chatbots', id=chatbot_row['id'], data={"no_answer_response": custom_no_answer})
    
    in_progress = {
        "status": {
            "label": "Model is Building"
        }
    }
    update_item = mndy.update_item(access_token=account_access['decrypted_monday_access_token'], board_id=board_id, item_id=item_id, column_values=json.dumps(json.dumps(in_progress)))
    logger.info(f'[MNDY_TRAIN_CHATBOT]: Updated chatbot to "Model is Building" : {decoded_header["accountId"]}')
    
    item_ids = mndy.get_item_ids(access_token=account_access['decrypted_monday_access_token'], board_id=chatbot_row['documents_board_id'])
    if not item_ids:
        logger.error('[MNDY_TRAIN_CHATBOT]: ERROR : No items in the documents board, or an issue occurred while getting items.') 
        data = {
            "status": {
                "label": "ERROR"
            },
            "long_text": {
                "text": "There are no items in the documents board or there was an issue getting the items. If there are items, please train the chatbot again"
            }
        }
        update_item = mndy.update_item(access_token=account_access['decrypted_monday_access_token'], board_id=board_id, item_id=item_id, column_values=json.dumps(json.dumps(data)))
        return return_success() # There are not documents or error, do something
    
    item_values = mndy.get_item_values_and_assets(access_token=account_access['decrypted_monday_access_token'], item_ids=item_ids)
    if not item_values: 
        logger.error('[MNDY_TRAIN_CHATBOT]: ERROR : No items in the documents board, or an issue occurred while getting items.') 
        data = {
            "status": {
                "label": "ERROR"
            },
            "long_text": {
                "text": "There are no items in the documents board or there was an issue getting the items. If there are items, please train the chatbot again"
            }
        }
        update_item = mndy.update_item(access_token=account_access['decrypted_monday_access_token'], board_id=board_id, item_id=item_id, column_values=json.dumps(json.dumps(data)))
        return return_success() # There are not documents or error, do something
        

    parsed_documents = []
    asset_ids = []
    logger.info(f'[MNDY_TRAIN_CHATBOT]: BEGIN PROCESSING ITEMS : {decoded_header["accountId"]}')
    for doc_item_id, values in item_values.items():
        if values['group']['id'] != chatbot_row['group_internal_name']:
            continue

        for asset in values['assets']:
            asset_ids.append(int(asset['id']))
        
        process = False
        do_not_include_source = False
        for column in values['column_values']:
            if column['id'] == 'status':
                if column['text'] not in ['Updated', 'New']:
                    continue
                else:
                    process = True
            elif column['id'] == 'checkbox':
                try:
                    value = json.loads(column['value'])
                    print(value)
                    do_not_include_source = value['checked']
                    if do_not_include_source in [True, 'true']:
                        do_not_include_source = True
                except:
                    do_not_include_source = False
        
        if not process:
            continue
        
        if not values['assets']:
            # Updated document status to new
            data = {
                "status": {
                    "label": "New"
                }
            }
            update_item = mndy.update_item(access_token=account_access['decrypted_monday_access_token'], board_id=chatbot_row['documents_board_id'], item_id=doc_item_id, column_values=json.dumps(json.dumps(data)))


        
        for i, asset in enumerate(values['assets']):
            try:
                document_name, document_type = asset['name'].rsplit('.', 1)
            except:
                document_name, document_type = None, None
                logger.error(f'[MNDY_TRAIN_CHATBOT]: ERROR : Could not split asset into name and type : Asset {asset} : {decoded_header["accountId"]}')
            
            parsed_document = {
                'monday_account_id': decoded_header['accountId'],
                'public_monday_url': asset['public_url'],
                'private_monday_url': asset['url'],
                'document_name': document_name,
                'document_type': document_type,
                'group_name': values['group']['id'],
                'file_name': asset['name'],
                'file_status': 'TO_PROCESS',
                'item_id': doc_item_id,
                'asset_id': asset['id'],
                'chatbot_db_id': chatbot_row['id'],
                'chatbot_item_id': item_id,
                'account_db_id': account['id'],
                'do_not_include_source': do_not_include_source
            }
            # try:
            #     next_item = values['assets'][i + 1]
            #     parsed_document['last_asset'] = False
            # except:
            #     parsed_document['last_asset'] = True
            parsed_documents.append(parsed_document)
            logger.info(f'[MNDY_TRAIN_CHATBOT]: Added document to process list : Document {parsed_document} : {decoded_header["accountId"]}')

    res = requests.post(
        url='https://qjvzg2dbk2jp7jiz4k3663ruyq0krape.lambda-url.us-east-1.on.aws/', 
        headers={'content-type': 'application/json'},
        data=json.dumps({'asset_ids': asset_ids, 'chatbot_id': chatbot_row['id']})
    )
    logger.info(f'[MNDY_TRAIN_CHATBOT]: Asset ids sent to determine any deletes needed : {decoded_header["accountId"]}')
    try:
        delete = res.json()['delete']
    except:
        delete = False

    if not parsed_documents and not delete:
        logger.info(f'[MNDY_TRAIN_CHATBOT]: No documents to send off and no deletes : {decoded_header["accountId"]}')
        # Create a chatbot training item and note that there was nothing to process
        column_values = {
            "status": "Completed",
            "long_text": "There were no new documents or documents to delete. Chatbot training is complete, but please ensure that this was expected. Refer to the documentation on common troubleshooting scenarios."
        }
        chat_training_item = mndy.create_item(access_token=decoded_header['shortLivedToken'], board_id=account['monday_training_board_id'], item_name=f'{chatbot_row["name"]}', column_values=column_values)
        try:
            chat_training_id = chat_training_item['data']['create_item']['id']
            logger.info(f'[MNDY_TRAIN_CHATBOT]: Successfully created completed chat training item in Monday : {decoded_header["accountId"]}')
        except:
            chat_training_id = None
            logger.error(f'[MNDY_TRAIN_CHATBOT]: ERROR : Could not create completed chat training item in Monday : {decoded_header["accountId"]}')

        data = {
            'chatbot_id': chatbot_row.get('id'),
            'status': 'COMPLETE',
            'name': chatbot_row.get('name'),
            'account_id': account.get('id'),
            'monday_account_id': account.get('monday_account_id'),
            'monday_board_id': account.get('monday_training_board_id'),
            'monday_item_id': chat_training_id
        }
        supa.insert(supabase=supabase, table_name='chatbot_trainings', data=data)
        logger.info(f'[MNDY_TRAIN_CHATBOT]: Inserted chat training row in supabase : {decoded_header["accountId"]}')
        supa.update_by_id(supabase=supabase, table_name='chatbots', id=chatbot_row['id'], data={"status": "COMPLETE"})
        logger.info(f'[MNDY_TRAIN_CHATBOT]: Update chatbot row in supabase to "COMPLETE" : {decoded_header["accountId"]}')
        mndy.update_item(access_token=decoded_header['shortLivedToken'], board_id=account['monday_chatbots_board_id'], item_id=chatbot_row['item_id'], column_values=json.dumps(json.dumps({'status': 'Completed'})))
        logger.info(f'[MNDY_TRAIN_CHATBOT]: Updated chatbot item in Monday to "Completed" : {decoded_header["accountId"]}')

    if delete and not parsed_documents:
        logger.info(f'[MNDY_TRAIN_CHATBOT]: Documents to Delete, but no documents to Add : {decoded_header["accountId"]}')
        data = {
            'chatbot_id': chatbot_row.get('id'),
            'status': 'READY',
            'name': chatbot_row.get('name'),
            'account_id': account.get('id'),
            'monday_account_id': account.get('monday_account_id'),
            'monday_board_id': account.get('monday_training_board_id')
        }
        supa.insert(supabase=supabase, table_name='chatbot_trainings', data=data)
        logger.info(f'[MNDY_TRAIN_CHATBOT]: Inserted chatbot training item to Supabase in "READY" status : {decoded_header["accountId"]}')

    logger.info(f'[MNDY_TRAIN_CHATBOT]: {len(parsed_documents)} Documents to send to Queue : {decoded_header["accountId"]}') 
    for doc in parsed_documents:
        # send to queue to download file into supabase
        if doc == parsed_documents[-1]:
            doc['last_asset'] = True
        else:
            doc['last_asset'] = False
        event = {
            'event': doc
        }
        message_send = sqs_client.send_message(QueueUrl=os.getenv('SQS_URL'), MessageBody=json.dumps(event))
        logger.info(f'[MNDY_TRAIN_CHATBOT]: Sent document to Training Queue : Message ID {message_send["MessageId"]} : {decoded_header["accountId"]}')
    return return_success()

    
def return_success():
    logger.info(f'[MNDY_TRAIN_CHATBOT]: END')
    return {
        'statusCode': 200,
        'body': json.dumps('Hello from Lambda!')
    }