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

sqs_client = boto3.client('sqs')
supabase: Client = create_client(os.getenv('SUPABASE_URL'), os.getenv('SUPABASE_KEY'))
logger = logging.getLogger()
logger.setLevel(logging.INFO) 

def lambda_handler(event, context):
    logger.info('[SLACK_BLOCK_HANDLER]: ENTER')
    timestamp = event['headers']['x-slack-request-timestamp']
    request_time = datetime.fromtimestamp(int(timestamp))

    if datetime.now() - request_time > timedelta(minutes=5):
        # If the request is older than 5 minutes, it could be a replay attack, so let's ignore it.
        return 'Please try command again'
    
    # SOMETIMES BODY IS IN BASE64, this will convert it if it is
    try:
        event['body'] = base64.b64decode(event['body']).decode('utf-8')
    except:
        pass
    
    # If in base64, then the body is also URL parametized and not in key/value format
    try:
        initial_body = urllib.parse.parse_qs(event['body'])
        event['body']  = {k: v[0] for k, v in initial_body.items()}
    except:
        logger.error('[SLACK_BLOCK_HANDLER]: ERROR : Cannot convert base64 request')

    # Sometimes the payload is not in key/value format
    try:
        event['body']['payload'] = json.loads(event['body']['payload'])
        payload = event['body']['payload']
    except:
        logger.error(f'[SLACK_BLOCK_HANDLER]: ERROR : Cannot convert base64 request : {event}')
        logger.info('[SLACK_BLOCK_HANDLER]: END')
        return {
            "statusCode": 200
        }
    
    # sig_basestring = f'v0:{timestamp}:{event["body"]}'

    # my_signature = hmac.new(bytes(os.getenv('SIGNING_SECRET') , 'utf-8'), bytes(sig_basestring , 'utf-8'), hashlib.sha256).hexdigest()

    # # Prefix with 'v0='
    # my_signature = f'v0={my_signature}'

    # slack_signature = event['headers']['x-slack-signature']

    # # Compare the signatures, using the hmac compare_digest function
    # if not hmac.compare_digest(my_signature, slack_signature):
    #     # hooray, the request came from Slack!
    #     print('in signature')
    #     return 'Please try the command again'

    # The block handler wil handle any user interaction. There is not always an action associated
    try:
        payload['actions'][0]['value']
    except:
        logger.info('[SLACK_BLOCK_HANDLER]: No action performed')
        logger.info('[SLACK_BLOCK_HANDLER]: END')
        return {
            "statusCode": 200
        }

    # If the action is not clicking the submit button, then we don't casre about it
    if payload['actions'][0]['action_id'] not in ['question_sent', 'question_sent_enter']:
        logger.info(payload['actions'])
        logger.info('[SLACK_BLOCK_HANDLER]: Action performed, but was not submitting question')
        logger.info('[SLACK_BLOCK_HANDLER]: END')
        return {
            "statusCode": 200            
        }

    values_dict = payload["state"]["values"]
    logger.info(values_dict)
    # Create a new dictionary to store the renamed keys
    new_values_dict = {}



    # Iterate over each key in the values dictionary
    for key, value in values_dict.items():
        # If the "static_select-action" key is in the sub-dictionary, replace the key with "chatbot"
        if "static_select-action" in value:
            new_values_dict["chatbot"] = value
        # If the "plain_text_input-action" key is in the sub-dictionary, replace the key with "question"
        elif "question_sent_enter" in value:
            new_values_dict["question"] = value

    payload["state"]["values"] = new_values_dict
    
    if payload["state"]["values"]["question"]['question_sent_enter']['value'] in ['', None]:
        logger.info('[SLACK_BLOCK_HANDLER]: No text entered in question box')
        logger.info('[SLACK_BLOCK_HANDLER]: END')
        return {
            "statusCode": 200
        }
        
    if payload['state']['values']['chatbot']['static_select-action']['selected_option'] in ['', None]:
        logger.info('[SLACK_BLOCK_HANDLER]: No chatbot selected')
        logger.info('[SLACK_BLOCK_HANDLER]: END')
        return {
            "message": "include a chatbot",
            "statusCode": 200
        }
    
    supabase.postgrest.schema('public')

    item = supabase.table('accounts').select('*').eq('slack_team_id', payload['team']['id']).execute()
    try:
        account = item.data[0]
    except:
        account = None
        logger.error(f"[SLACK_BLOCK_HANDLER]: ERROR : Could not return account from supabase for slack team: {payload['team']['id']}")

    if not account:
        logger.info('[SLACK_BLOCK_HANDLER]: END')
        return {
            'statusCode': 200,
            'body': json.dumps('There is an error finding your account')
        }
    logger.info(f"[SLACK_BLOCK_HANDLER]: Start building new message : {payload['team']['id']}")
    blocks = [
        {
            "type": "section",
            "text": {
                "type": "mrkdwn",
                "text": ":question::page_facing_up::thumbsup:"
            }
        },
        {
            "type": "section",
            "text": {
                "type": "mrkdwn",
                "text": "Your question has been sent! Please allow a few seconds for the yak to think :bulb::brain: and a response will be added to this thread!"
            }
        },
        {
            "type": "section",
            "text": {
                "type": "mrkdwn",
                "text": f"*YakBot*: {payload['state']['values']['chatbot']['static_select-action']['selected_option']['text']['text']}"
            }
        },
        {
            "type": "section",
            "text": {
                "type": "mrkdwn",
                "text": f"*Question*: {payload['state']['values']['question']['question_sent_enter']['value']}"
            }
        }
    ]

    url = 'https://slack.com/api/chat.update'
    headers = {
            'Authorization': f'Bearer {account["token"]}',
            'Content-type': 'application/json'
    }
    body = {
            "channel": payload["channel"]['id'],
            "ts": payload['container']['message_ts'],
            "blocks": blocks
    }
    logger.info(f"[SLACK_BLOCK_HANDLER]: Reformatted block so that it shows the selected chatbot and question: {payload['team']['id']}")
    res = requests.post(url=url, headers=headers, json=body)
    chatbot_message = None
    try:
        chatbot = supabase.table('chatbots').select('*').eq('account_id', account['id']).eq('index_internal_name', payload['state']['values']['chatbot']['static_select-action']['selected_option']['value']).limit(1).single().execute()
        chatbot_message = chatbot.data['no_answer_response']
    except:
        logger.info(f'[SLACK_BLOCK_HANDLER] : SHould be generic chatgpt : body event {payload} : {account["id"]}')    

    slack_record = {
        "question": payload['state']['values']['question']['question_sent_enter']['value'],
        "chatbot" : payload['state']['values']['chatbot']['static_select-action']['selected_option']['value'],
        "chatbot_message": chatbot_message,
        "question": payload['state']['values']['question']['question_sent_enter']['value'],
        "chatbot" : payload['state']['values']['chatbot']['static_select-action']['selected_option']['value'],
        "channel_id": payload['container']['channel_id'],
        "slack_team_id": payload['team']['id'],
        "message_ts": payload['message']['ts'],
        "user_id": payload['user']['id'],
        "original_question": True,
        "command": "yak"
    }

    event = {
        'event': slack_record
    }
    message_send = sqs_client.send_message(QueueUrl=os.getenv('SQS_URL'), MessageBody=json.dumps(event), MessageGroupId='slack', MessageDeduplicationId=str(uuid.uuid4()))
    logger.info(f"[SLACK_BLOCK_HANDLER]: Sent Chatbot {slack_record['chatbot']} and Question {slack_record['question']} to Queue: {payload['team']['id']}")

    logger.info('[SLACK_BLOCK_HANDLER]: END')
    return {
        'statusCode': 200
    }
