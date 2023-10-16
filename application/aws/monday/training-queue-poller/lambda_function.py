import json
import jwt
import os
from supabase import create_client, client
import lib.supa as supa
from lib.types import TrainingDocQueueMsg
import lib.mndy as mndy
import lib.helpers as help
import json
import boto3
import logging

sqs_client = boto3.client('sqs')
supabase: client = create_client(os.getenv('SUPABASE_URL'), os.getenv('SUPABASE_KEY'))
logger = logging.getLogger()
logger.setLevel(logging.INFO)

def lambda_handler(event, context):
    logger.info('[MNDY_TRAINING_QUEUE_POLLER]: ENTER')
    messages = event['Records']
    reorder, idx = False, 0
    for i, message in enumerate(messages):
        message_body = json.loads(message['body'])
        if message_body['event']['last_asset'] and message != messages[-1]:
            reorder = True
            idx = i
            break
    
    if reorder:
        logger.info('Reordering messages')
        item = messages.pop(idx)
        messages.append(item)
    
    logger.info('[MNDY_TRAINING_QUEUE_POLLER]: Begin processing messages')
    for message in messages:
        message_body = json.loads(message['body'])
        training_doc = TrainingDocQueueMsg(**message_body['event'])
        logger.info(f'[MNDY_TRAINING_QUEUE_POLLER]: Processing Message {training_doc} : {training_doc.monday_account_id}')
        receipt_handle = message['receiptHandle']

        delete_message = sqs_client.delete_message(
            QueueUrl=os.getenv('SQS_URL'),
            ReceiptHandle=receipt_handle
        )

        # Loop through the messages which are documents
        # 
        bucket = supa.get_bucket(supabase=supabase, bucket_name=training_doc.monday_account_id)
        if not bucket:
            bucket = supa.create_bucket(supabase=supabase, bucket_name=training_doc.monday_account_id)
            logger.info(f'[MNDY_TRAINING_QUEUE_POLLER]: Created bucket: {bucket} : {training_doc.monday_account_id}')
        
        document_row = supa.get_one_by_id(supabase=supabase, table_name='documents', id=training_doc.asset_id)
        if not document_row:
            supa_file_path = f'{training_doc.group_name}/{training_doc.asset_id}_{training_doc.file_name}'
            local_file_path = f'/tmp/{training_doc.file_name}'
            logger.info(f'[MNDY_TRAINING_QUEUE_POLLER]: Downloading file locally {local_file_path}  : {training_doc.monday_account_id}')
            local_file_object = help.download_file(
                url=training_doc.public_monday_url,
                local_filename=local_file_path
            )
            content_type = {
                'doc': 'application/msword',
                'docx': 'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
                'txt': 'text/plain',
                'pdf': 'application/pdf',
                'csv': 'text/csv',
                'xls': 'application/vnd.ms-excel',
                'xlsx': 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
            }
            file_content_type = content_type.get(training_doc.document_type.lower(), None)
            if not file_content_type:
                account = supa.get_account(supabase=supabase, monday_account_id=training_doc.monday_account_id)
                account_access = supa.get_account_token(supabase=supabase, account_id=account['id'])
                column_values = {
                    "status": "ERROR",
                    "long_text": "File type not supported. Currently available types are pdf, doc, docx, txt, xls, xlsx, csv"
                }
                column_values_cb = {
                    "status": "ERROR",
                    "long_text": "Not all files processed. At least one included in training attempt that is not supported. Currently available types are pdf, doc, docx, txt, xls, xlsx, csv. Please see the documents board for further information."
                }
                mndy.update_item(access_token=account_access['decrypted_monday_access_token'], board_id=account['monday_documents_board_id'], item_id=training_doc.item_id, column_values=json.dumps(json.dumps(column_values)))
                mndy.update_item(access_token=account_access['decrypted_monday_access_token'], board_id=account['monday_chatbots_board_id'], item_id=training_doc.chatbot_item_id, column_values=json.dumps(json.dumps(column_values_cb)))
                logger.info(f'[MNDY_TRAINING_QUEUE_POLLER]: Unsupported file type {local_file_path}  : {training_doc.monday_account_id}')
                continue
            logger.info(f'[MNDY_TRAINING_QUEUE_POLLER]: Uploading file to Supabase {local_file_path}  : {training_doc.monday_account_id}')
            supa_file_object = supa.create_bucket_object(
                supabase=supabase,
                bucket_name=training_doc.monday_account_id, 
                path=supa_file_path,
                file_contents=local_file_object,
                file_content_type=file_content_type
            )
            
            logger.info(f'[MNDY_TRAINING_QUEUE_POLLER]: Deleting file locally {local_file_path}  : {training_doc.monday_account_id}')
            help.delete_local_file(local_file_path)

            supa_storage_row = supa.get_object_row_by_name_and_bucket(
                supabase=supabase,
                bucket_id=training_doc.monday_account_id,
                path=supa_file_path
            )

            document = {
                'id': training_doc.asset_id,
                'document_name': training_doc.document_name,
                'document_type': training_doc.document_type,
                'public_monday_url': training_doc.public_monday_url,
                'bucket_location': training_doc.monday_account_id,
                'document_object': supa_storage_row['id'],
                'private_monday_url': training_doc.private_monday_url,
                'monday_account_id': training_doc.monday_account_id,
                'group_name': training_doc.group_name,
                'file_name': training_doc.file_name,
                'file_status': 'INSERT',
                'chatbot_id': training_doc.chatbot_db_id,
                'item_id': training_doc.item_id                
            }
            document_row = supa.insert(supabase=supabase, table_name='documents', data=document)
            logger.info(f'[MNDY_TRAINING_QUEUE_POLLER]: Document {training_doc.asset_id} (monday asset id) inserted into the database : {training_doc.monday_account_id}')

    # Check if last
    last_message = messages[-1]
    last_message_body = json.loads(last_message['body'])
    if last_message_body['event']['last_asset']:
        last_doc = TrainingDocQueueMsg(**last_message_body['event'])
        data = {
            'chatbot_id': last_doc.chatbot_db_id,
            'status': 'READY',
            'name': last_doc.group_name,
            'account_id': last_doc.account_db_id,
            'monday_account_id': last_doc.monday_account_id,
        }
        data = supa.insert(supabase=supabase, table_name='chatbot_trainings', data=data)
        logger.info(f'[MNDY_TRAINING_QUEUE_POLLER]: Inserted chatbot training row in Supabase with status of "Ready" ')


    logger.info(f'[MNDY_TRAINING_QUEUE_POLLER]: END')
    return {
        'statusCode': 200,
        'body': json.dumps('Hello from Lambda!')
    }