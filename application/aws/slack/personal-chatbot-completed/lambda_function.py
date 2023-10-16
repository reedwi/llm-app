import json
from supabase import Client, create_client
import requests
from pprint import pprint
import os
import hashlib
import hmac
import base64
import urllib.parse
from datetime import datetime, timedelta
import boto3
import uuid
import logging
import re

supabase: Client = create_client(os.getenv('SUPABASE_URL'), os.getenv('SUPABASE_KEY'))
logger = logging.getLogger()
logger.setLevel(logging.INFO) 

def lambda_handler(event, context):
    logger.info('[PERSONAL_CHATBOT_COMPLETED]: ENTER')
    authorization = event['headers'].get('authorization', None)
    if not authorization or authorization != os.getenv('SUPABASE_AUTH_HEADER'):
        logger.info(f'[PERSONAL_CHATBOT_COMPLETED]: Not authorized :END ')  
        return {
            'statusCode': 422,
            'body': json.dumps('Unauthorized')
        }
        
    try:
        payload = json.loads(event['body'])
    except:
        payload = None
        logger.info(f'[PERSONAL_CHATBOT_COMPLETED]: No payload :END ')  
        return {
            'statusCode': 200,
            'body': json.dumps('No payload present')
        }
    
    if payload['old_record']['status'] != 'COMPLETE' and payload['record']['status'] == 'COMPLETE':
        logger.info(f'[PERSONAL_CHATBOT_COMPLETED]: Meets entry criteria : ')  
    else:
        logger.info(f'[PERSONAL_CHATBOT_COMPLETED]: Does not meet entry criteria :END ')  
        return {
            'statusCode': 200,
            'body': json.dumps('Does not satisfy entry requirements')
        }
    supabase.postgrest.schema('public')

    item = supabase.table('accounts').select('*').eq('id', payload['record']['account_id']).execute()
    try:
        account = item.data[0]
    except:
        account = None
        logger.error(f"[PERSONAL_CHATBOT_COMPLETED]: ERROR : Could not return account from supabase for account: {payload['record']['account_id']}")
        
    item = supabase.table('documents').select('*').eq('personal_chatbot_id', payload['record']['id']).eq('file_status', 'COMPLETE').execute()
    try:
        files = item.data
    except:
        files = None
        logger.error(f"[PERSONAL_CHATBOT_COMPLETED]: ERROR : Could not return files for personal chatbot: {payload['record']['account_id']}")
        
    logger.info(f"[PERSONAL_CHATBOT_COMPLETED]: Start building new message : {payload['record']['account_id']}")
    blocks = [
        {
            "type": "section",
            "text": {
                "type": "mrkdwn",
                "text": ":open_file_folder::arrow_up:"
            }
        },
        {
            "type": "section",
            "text": {
                "type": "mrkdwn",
                "text": "Your YakBot is ready!"
            }
        },
        {
            "type": "section",
            "text": {
                "type": "mrkdwn",
                "text": f"*Files Available*: {', '.join([file['document_name'] for file in files])}"
            }
        },
        {
            "type": "section",
            "text": {
                "type": "mrkdwn",
                "text": f"You may now ask questions of these file(s) within the thread!"
            }
        }
    ]

    url = 'https://slack.com/api/chat.update'
    headers = {
            'Authorization': f'Bearer {account["token"]}',
            'Content-type': 'application/json'
    }
    body = {
            "channel":payload['record']['channel_id'],
            "ts": payload['record']['thread_ts'],
            "blocks": blocks
    }
    logger.info(f"[PERSONAL_CHATBOT_COMPLETED]: Reformatted block so that it shows the selected chatbot and question: {payload['record']['account_id']}")
    res = requests.post(url=url, headers=headers, json=body)
    logger.info(f'[PERSONAL_CHATBOT_COMPLETED]: {res.text}')
    
    chat_history = get_thread_history(slack_key=account['token'], channel_id=payload['record']['channel_id'], thread_ts=payload['record']['thread_ts'])
    last_message = chat_history[-1]
    delete_slack_message(slack_key=account['token'], channel_id=payload['record']['channel_id'], message_ts=last_message["ts"])
    yak_text = ":white_check_mark: The newly created YakBot is ready. Please ask questions in this thread and the yak will answer :brain::bulb:"
    reply = reply_in_thread(slack_key=account['token'], channel_id=payload['record']['channel_id'], thread_ts=payload['record']['thread_ts'], text=yak_text)
    # TODO implement
    return {
        'statusCode': 200,
        'body': json.dumps('Hello from Lambda!')
    }


def get_thread_history(slack_key, channel_id, thread_ts):
    headers = {
        'content-type': 'application/json',
        'Authorization': f'Bearer {slack_key}'
    }
    params = {
        'channel': channel_id,
        'ts': thread_ts
    }
    res = requests.get(url='https://slack.com/api/conversations.replies', headers=headers, params=params)

    if not res.ok:
        return None
    
    res_json = res.json()
    if not res_json['ok']:
        return None

    message_thread = []
    for message in res_json['messages']:
        if 'bot_id' in message:
            message_parse = {
                "bot": True,
                "ts": message['ts'],
                "text": message['text']
            }
        else:
            message_parse = {
                "bot": False,
                "ts": message['ts'],
                "text": message['text']
            }
        try:
            message_parse['files'] = message['files']
        except:
            pass
        message_thread.append(message_parse)
    return message_thread
    
def delete_slack_message(slack_key, channel_id, message_ts):
    url = "https://slack.com/api/chat.delete"

    data = {
        "channel": channel_id,  # The ID of the channel where the message is posted.
        "ts": message_ts  # The 'ts' value of the message to reply to.
    }

    headers = {
        "Content-type": "application/json; charset=utf-8",
        "Authorization": f"Bearer {slack_key}"
    }

    response = requests.post(url, headers=headers, json=data)
    
def reply_in_thread(slack_key, channel_id, thread_ts, text):

    url = "https://slack.com/api/chat.postMessage"
    try:
        message = format_message(message=text)
    except:
        message = text
    data = {
        "channel": channel_id,  # The ID of the channel where the message is posted.
        "text": message,  # The text of the message to post.
        "thread_ts": thread_ts  # The 'ts' value of the message to reply to.
    }

    headers = {
        "Content-type": "application/json; charset=utf-8",
        "Authorization": f"Bearer {slack_key}"
    }

    response = requests.post(url, headers=headers, json=data)
    return response

def format_message(message):
    REGEX_REPLACE = (
        (re.compile('^- ', flags=re.M), '• '),
        (re.compile('^  - ', flags=re.M), '  ◦ '),
        (re.compile('^    - ', flags=re.M), '    ⬩ '), # ◆
        (re.compile('^      - ', flags=re.M), '    ◽ '),
        (re.compile('^#+ (.+)$', flags=re.M), r'*\1*'),
        (re.compile('\*\*'), '*'),
    ) 
    for regex, replacement in REGEX_REPLACE:
        message = regex.sub(replacement, message)
    return message