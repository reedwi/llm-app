import boto3
import json
import os
from urllib.parse import quote
from .obo_langchain import get_answer
from .obo_slack import get_thread_history, reply_in_thread, delete_slack_message
from .slack_commands import yak, yak_files
from supabase import Client, create_client

sqs_client = boto3.client('sqs')
supabase: Client = create_client(os.getenv('SUPABASE_URL'), os.getenv('SUPABASE_KEY'))

def lambda_handler(event, context):
    # TODO implement
    print('[SLACK_QUEUE_POLLER]: ENTER')
    messages = event['Records']
    print('[SLACK_QUEUE_POLLER]: START PROCESSING QUEUE MESSAGES')
    for message in messages:
        message_body = json.loads(message['body'])
        
        slack_team_id = message_body['event']['slack_team_id']
        namespace = message_body['event']['chatbot']
        message_ts = message_body['event']['message_ts']
        question = message_body['event']['question']
        original_question = message_body['event']['original_question']
        channel_id = message_body['event']['channel_id']
        user_id = message_body['event']['user_id']
        command = message_body['event']['command']
        chatbot_message = message_body['event'].get('chatbot_message')
        print(f'[SLACK_QUEUE_POLLER]: Message Start : {slack_team_id}')

        receipt_handle = message['receiptHandle']
        delete_message = sqs_client.delete_message(
            QueueUrl=os.getenv('SQS_URL'),
            ReceiptHandle=receipt_handle
        )

        supabase.postgrest.schema('public')

        item = supabase.table('accounts').select('*').eq('slack_team_id', slack_team_id).execute()
        try:
            account = item.data[0]
        except:
            account = None
            print(f'[SLACK_QUEUE_POLLER]: ERROR : Could not return account from supabase : {slack_team_id}')

        if not account:
            print(f'[SLACK_QUEUE_POLLER]: END : {slack_team_id}')
            return {
                'statusCode': 200,
                'body': json.dumps('There is an error finding your account')
            }

        
        if command == 'yak':
            print(f'[SLACK_QUEUE_POLLER]: Getting answer : {slack_team_id}')
            if original_question:
                chat_history = None
                yak_message = None
            else:
                yak_text = ":bulb::brain: the yak is thinking, one moment please :brain::bulb:"
                chat_history = get_thread_history(slack_key=account['token'], channel_id=channel_id, thread_ts=message_ts)
                loading = reply_in_thread(slack_key=account['token'], channel_id=channel_id, thread_ts=message_ts, text=yak_text)
                try:
                    yak_message = loading.json()['ts']
                except:
                    yak_message = None
            data = {
                "namespace": namespace,
                "question": question,
                "chat_history": chat_history,
                "slack_key": account['token'],
                "channel_id": channel_id,
                "thinking_ts": yak_message,
                "message_ts": message_ts,
                "slack_team_id": slack_team_id,
                "account_id": account['id'],
                "chatbot_message": chatbot_message
            }
            success = yak(data, supabase)
        
        elif command == 'yak_files':
            chat_history = get_thread_history(slack_key=account['token'], channel_id=channel_id, thread_ts=message_ts)
            if original_question:
                yak_text = ":recycle::brain: the yak is busy ingesting files, please give us a few moments (seconds to minutes) to do this properly and we will notify you when ready :brain::recycle:"
            else:
                yak_text = ":bulb::brain: the yak is thinking, one moment please :brain::bulb:"
            loading = reply_in_thread(slack_key=account['token'], channel_id=channel_id, thread_ts=message_ts, text=yak_text)
            try:
                yak_message = loading.json()['ts']
            except:
                yak_message = None
            
            
            data = {
                "namespace": namespace,
                "question": question,
                "chat_history": chat_history,
                "slack_key": account['token'],
                "channel_id": channel_id,
                "thinking_ts": yak_message,
                "message_ts": message_ts,
                "slack_team_id": slack_team_id,
                "account_id": account['id'],
                "original_question": original_question,
                "user_id": user_id
            }
            answer_obj = yak_files(data, supabase)
    
    
    print(f'[SLACK_QUEUE_POLLER]: END')  
    return {
        'statusCode': 200,
        'body': json.dumps('Hello from Lambda!')
    }

