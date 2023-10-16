import json
import requests
from supabase import Client, create_client
import os
import uuid
import boto3
import logging

sqs_client = boto3.client('sqs')
supabase: Client = create_client(os.getenv('SUPABASE_URL'), os.getenv('SUPABASE_KEY'))
logger = logging.getLogger()
logger.setLevel(logging.INFO) 

def lambda_handler(event, context):
    logger.info('[SLACK_MENTION_EVENT]: ENTER')
    body = json.loads(event['body'])
    logger.info(body)
    if 'bot_profile' in body["event"]:
        logger.info('[SLACK_MENTION_EVENT]: Bot profile event')
        logger.info('[SLACK_MENTION_EVENT]: END')
        return {
            'statusCode': 200,
        }
    elif 'hidden' in body["event"]:
        logger.info('[SLACK_MENTION_EVENT]: Hidden event')
        logger.info('[SLACK_MENTION_EVENT]: END')
        return {
            'statusCode': 200,
        }
    elif 'bot_id' in body["event"]:
        logger.info('[SLACK_MENTION_EVENT]: Bot_id event')
        logger.info('[SLACK_MENTION_EVENT]: END')
        return {
            'statusCode': 200,
        }
    elif 'thread_ts' not in body["event"]:
        supabase.postgrest.schema('public')

        item = supabase.table('accounts').select('*').eq('slack_team_id', body['team_id']).execute()
        try:
            account = item.data[0]
        except:
            account = None
            logger.error(f'[SLACK_MENTION_EVENT]: ERROR : Could not return account from supabase for slack team id: {body["team_id"]}')
        url = "https://slack.com/api/chat.postMessage"

        data = {
            "channel": body['event']['channel'],  # The ID of the channel where the message is posted.
            "text": "Please use the /yak or /yak_personal slash command to initiate a question",  # The text of the message to post.
            "thread_ts": body['event']['ts']  # The 'ts' value of the message to reply to.
        }

        headers = {
            "Content-type": "application/json; charset=utf-8",
            "Authorization": f"Bearer {account['token']}"
        }
        response = requests.post(url, headers=headers, json=data)
        logger.info(f'[SLACK_MENTION_EVENT]: Sent error message saying to use the /yak command : {body["team_id"]}')
        logger.info('[SLACK_MENTION_EVENT]: END')
        return {
            "statusCode": 200,
        }
    else:
        time_stamp = body["event"].get('thread_ts', None)
    
    supabase.postgrest.schema('public')

    item = supabase.table('accounts').select('*').eq('slack_team_id', body['team_id']).execute()
    try:
        account = item.data[0]
    except:
        account = None
        logger.error(f'[SLACK_MENTION_EVENT]: ERROR : Could not return account from supabase for slack team id: {body["team_id"]}')

    if not account:
        logger.info(f"[SLACK_MENTION_EVENT]: END : {body['team_id']}")
        return {
            'statusCode': 200,
            'body': json.dumps('There is an error finding your account')
        }

    if account.get('account_status') == 'EXPIRED':
        url = 'https://slack.com/api/chat.postMessage'
        headers = {
                'Authorization': f'Bearer {account["token"]}',
                'Content-type': 'application/json'
        }
        data = {
            "channel": body['event']['channel'],  # The ID of the channel where the message is posted.
            "text": ":hourglass: You have either reached your account limits for the month or are no longer subscribed. Please reach out to your account admin to upgrade or renew your account!",  # The text of the message to post.
            "thread_ts": body['event']['ts'] 
        }
        res = requests.post(url=url, headers=headers, json=data)
        logger.info(f"[SLACK_MENTION_EVENT]: Account Over Limits : {body['team_id']}")
        return {
            'statusCode': 200
        }

    headers = {
        'content-type': 'application/json',
        'Authorization': f'Bearer {account["token"]}'
    }
    params = {
        'channel': body['event']['channel'],
        'ts': time_stamp
    }
    logger.info(f'[SLACK_MENTION_EVENT]: Getting thread history : {body["team_id"]}')
    res = requests.get(url='https://slack.com/api/conversations.replies', headers=headers, params=params)
    if not res.ok:
        logger.error(f'[SLACK_MENTION_EVENT]: ERROR : Could not get thread history: {body["team_id"]}')
        logger.info('[SLACK_MENTION_EVENT]: END')
        return {
            "statusCode": 200,
        }
    
    res_json = res.json()
    if not res_json['ok']:
        logger.error(f'[SLACK_MENTION_EVENT]: ERROR : Could not get thread history: {body["team_id"]}')
        logger.info('[SLACK_MENTION_EVENT]: END')
        return {
            "statusCode": 200,
        }
        
    initial_question = res_json['messages'][0]
    messages = res_json['messages']

    if initial_question['text'].startswith(':question::page_facing_up:'):
        start_index = initial_question['text'].find("*YakBot*: ") + len("*YakBot*: ")
        end_index = initial_question['text'].find(" *Question*:")
        chatbot_name = initial_question['text'][start_index:end_index].strip()
        chatbot_message = None
        if chatbot_name == 'ChatGPT':
            chatbot_internal = 'chatgpt'
        else:
            logger.info(f'[SLACK_MENTION_EVENT]: CHATBOT NAME: {chatbot_name}, ACCOUNT ID: {account["id"]}')
            try:
                chatbot = supabase.table('chatbots').select('*').eq('account_id', account['id']).eq('name', chatbot_name).limit(1).single().execute()
                chatbot_internal = chatbot.data['index_internal_name']
                chatbot_message = chatbot.data['no_answer_response']
            except:
                logger.error(f'[SLACK_MENTION_EVENT]: ERROR : Error when trying to get chatb : body event {body["event"]} : chatbot_name: {chatbot_name} : {body["team_id"]}')
                
        slack_record = {
            "question": body['event']['text'],
            "chatbot" : chatbot_internal,
            "chatbot_message": chatbot_message,
            "channel_id": body['event']['channel'],
            "slack_team_id": body['team_id'],
            "user_id": body['event']['user'],
            "message_ts": time_stamp,
            "original_question": False,
            "command": "yak"
        }
        logger.info('in regular question')
    elif initial_question['text'].startswith(':open_file_folder::arrow_up:'):
        if len(messages) == 2:
            try:
                files = messages[1]['files']
                slack_record = {
                    "question": body['event']['text'],
                    "chatbot" : None,
                    "channel_id": body['event']['channel'],
                    "slack_team_id": body['team_id'],
                    "user_id": body['event']['user'],
                    "message_ts": time_stamp,
                    "original_question": True,
                    "command": "yak_files"
                }
            except:
                data = {
                    "channel": body['event']['channel'],  # The ID of the channel where the message is posted.
                    "text": ":rotating_light:There are no files attached to your message. Please run '/yak_files' again and make sure to attach files in your response to the thread:rotating_light:",  # The text of the message to post.
                    "thread_ts": body['event']['ts']  # The 'ts' value of the message to reply to.
                }
        
                headers = {
                    "Content-type": "application/json; charset=utf-8",
                    "Authorization": f"Bearer {account['token']}"
                }
                url = "https://slack.com/api/chat.postMessage"
                response = requests.post(url, headers=headers, json=data)
                slack_record = None
            
        else:
            print('follow up question')
            namespace = f"{body['event']['user']}_{time_stamp.replace('.', '')}"
            slack_record = {
                "question": body['event']['text'],
                "chatbot" : namespace,
                "channel_id": body['event']['channel'],
                "slack_team_id": body['team_id'],
                "user_id": body['event']['user'],
                "message_ts": time_stamp,
                "original_question": False,
                "command": "yak_files"
            }

    if slack_record:
        event = {
            'event': slack_record
        }
        
        logger.info(f'[SLACK_MENTION_EVENT]: Sending message to queue {slack_record} : {body["team_id"]}')
        
        message_send = sqs_client.send_message(QueueUrl=os.getenv('SQS_URL'), MessageBody=json.dumps(event), MessageGroupId='slack', MessageDeduplicationId=str(uuid.uuid4()))
        logger.info(f'[SLACK_MENTION_EVENT]: END : {body["team_id"]}')
    return {
        'statusCode': 200
    }


