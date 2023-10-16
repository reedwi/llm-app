import json
from supabase import Client, create_client
import requests
import os
import hashlib
import hmac
import base64
import urllib.parse
from datetime import datetime, timedelta
import logging

supabase: Client = create_client(os.getenv('SUPABASE_URL'), os.getenv('SUPABASE_KEY'))
logger = logging.getLogger()
logger.setLevel(logging.INFO) 

def lambda_handler(event, context):
    logger.info('[SLACK_FILES_SLASH_COMMAND]: ENTER')
    if event['isBase64Encoded']:
        event['body'] = base64.b64decode(event['body']).decode('utf-8')
        
    # event['body'] = json.loads(event['body'])
    timestamp = event['headers']['x-slack-request-timestamp']
    request_time = datetime.fromtimestamp(int(timestamp))

    if datetime.now() - request_time > timedelta(minutes=5):
        # If the request is older than 5 minutes, it could be a replay attack, so let's ignore it.
        return 'Please try command again'
    
    sig_basestring = f'v0:{timestamp}:{event["body"]}'

    my_signature = hmac.new(bytes(os.getenv('SIGNING_SECRET') , 'utf-8'), bytes(sig_basestring , 'utf-8'), hashlib.sha256).hexdigest()

    # Prefix with 'v0='
    my_signature = f'v0={my_signature}'

    slack_signature = event['headers']['x-slack-signature']

    # Compare the signatures, using the hmac compare_digest function
    if not hmac.compare_digest(my_signature, slack_signature):
        # hooray, the request came from Slack!
        return 'Please try the command again'
    
    try:
        initial_body = urllib.parse.parse_qs(event['body'])
        event['body']  = {k: v[0] for k, v in initial_body.items()}
    except:
        logger.error('[SLACK_FILES_SLASH_COMMAND]: ERROR : Cannot convert base64 request')
    
    supabase.postgrest.schema('public')

    item = supabase.table('accounts').select('*').eq('slack_team_id', event['body']['team_id']).execute()

    try:
        account = item.data[0]
    except:
        account = None
        logger.error(f"[SLACK_FILES_SLASH_COMMAND]: ERROR : Cannot get account : {event['body']['team_id']}")

    if not account:
        logger.info(f"[SLACK_FILES_SLASH_COMMAND]: END : {event['body']['team_id']}")
        return {
            'statusCode': 200,
            'body': json.dumps('There is an error finding your account')
        }
    
    if account['account_status'] == 'EXPIRED':
        logger.info(f"[SLACK_FILES_SLASH_COMMAND]: Account Over Limits : {event['body']['team_id']}")
        return {
            'statusCode': 200,
            'body': ":hourglass: You have either reached your account limits for the month or are no longer subscribed. Please reach out to your account admin to upgrade or renew your account!"
        }
    
    # supabase.postgrest.schema('public')
    # items = supabase.table('chatbots').select('*').eq('account_id', account['id']).eq('status', 'COMPLETE').neq('index_internal_name', None).neq('index_internal_name', '').execute()
    # try:
    #     chatbots = items.data
    # except:
    #     chatbots = None

    logger.info(f"[SLACK_FILES_SLASH_COMMAND]: Building Block Kit : {event['body']['team_id']}")

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
                "text": "*Please reply to this thread and attach the file(s) you wish to chat with*. YakBots will then begin building your personal YakBot. \nThis can take some time (seconds - multiple minutes), but we will notify you in the thread when ready!"
            }
        },
        {
            "type": "section",
            "text": {
                "type": "mrkdwn",
                "text": "*Accepted File Formats*: .doc | .docx | .txt | .pdf | .csv | .xls | .xslx \n*Multiple File Attachment?*: You may attach multiple files in the reply to this thread, but this use is intended for smaller, quick tasks \n*Expiration*: This thread will work for ~7 days once generated" 
            }
        },
        {
			"type": "image",
			"image_url": "https://imucfdocuryhngcxutua.supabase.co/storage/v1/object/public/yakbots-media/ezgif.com-video-to-gif.gif?t=2023-08-17T21%3A48%3A25.567Z",
			"alt_text": "how-to"
		}
    ]

    url = 'https://slack.com/api/chat.postMessage'
    headers = {
            'Authorization': f'Bearer {account["token"]}',
            'Content-type': 'application/json'
    }
    body = {
            "channel": event["body"]["channel_id"],
            "blocks": blocks
        }
    logger.info(f"[SLACK_FILES_SLASH_COMMAND]: Block send request : {body}")
    res = requests.post(url=url, headers=headers, json=body)
    logger.info(f"[SLACK_FILES_SLASH_COMMAND]: Block send response : {res.text}")
    logger.info(f"[SLACK_FILES_SLASH_COMMAND]: Sent Block Kit Response : {event['body']['team_id']}")

    if not res.ok:
        logger.error(f'[SLACK_FILES_SLASH_COMMAND]: ERROR : Issue displaying block kit for slack team: {event["body"]["team_id"]} and channel_id: {event["body"]["channel_id"]}\nResponse: {res.text}')
    
    logger.info(f"[SLACK_FILES_SLASH_COMMAND]: END : {event['body']['team_id']}")
    return {
        'statusCode': 200
    }
