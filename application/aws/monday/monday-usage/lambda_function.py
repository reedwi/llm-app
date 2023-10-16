import json
import requests
import os
import lib.supa as supa
import json
import lib.mndy as mndy
from supabase import client, create_client
import logging

supabase: client = create_client(os.getenv('SUPABASE_URL'), os.getenv('SUPABASE_KEY'))
logger = logging.getLogger()
logger.setLevel(logging.INFO)

def lambda_handler(event, context):
    logger.info('[MNDY_TOKEN_USAGE]: ENTER')
    event['body'] = json.loads(event['body'])
    account = supa.get_one_by_id(supabase=supabase, table_name='accounts', id=event['body']['record']['account_id'])
    if not account:
        logger.error(f"[MNDY_TOKEN_USAGE]: ERROR : Cannot find a corresponding account in the account table for account: {event['body']['record']['account_id']}")
        return return_success()
    logger.info(f'[MNDY_TOKEN_USAGE]: START : {account["monday_account_id"]}')

    account_access = supa.get_account_token(supabase=supabase, account_id=account['id'])
    if not account_access:
        logger.error(f"[MNDY_TOKEN_USAGE]: ERROR : Cannot find a corresponding account token in the account table for account: {event['body']['record']['account_id']}")
        return return_success()
    
    if event['body']['record']['index_namespace'] == 'chatgpt':
        chatbot_name = 'ChatGPT'
    else:
        supabase.postgrest.schema('public')
        chatbot_rows = supabase.table('chatbots').select('*').eq("account_id", event['body']['record']['account_id']).eq("index_internal_name", event['body']['record']['index_namespace']).execute()
        try:
            chatbot = chatbot_rows.data[0]
            chatbot_name = chatbot['name']
        except:
            logger.info(f"[MNDY_TOKEN_USAGE]: ERROR : Cannot find a corresponding chatbot with index_internal_name of {event['body']['record']['index_namespace']} : {event['body']['record']['account_id']}")
            chatbot_name = None
    column_values = {
        "text": chatbot_name,
        "text5": f"{event['body']['record']['prompter']}",
        "long_text": {"text": f"{event['body']['record']['prompt']}"},
        "long_text9": f"{event['body']['record']['answer']}",
        "numbers": event['body']['record']['tokens_used']
    }

    item_name = f"{event['body']['record']['prompt'][:27]}..."
    headers = {
        "Authorization": f"Bearer {account_access['decrypted_monday_access_token']}",
        "Content-Type": "application/json"
    }
    query = f'''
        mutation {{
            create_item (board_id: {account['monday_usage_board_id']}, item_name: "{item_name}", column_values: {json.dumps(json.dumps(column_values))} ) {{
                id
            }}
        }}
    '''
    data = {'query': query}
    r = requests.post(
        url='https://api.monday.com/v2',
        headers=headers,
        json=data
    )
    try:
        r_json = r.json()
        logger.info(f"[MNDY_TOKEN_USAGE]: Succesfully created Usage item : {account['monday_account_id']}")
    except:
        logger.error(f"[MNDY_TOKEN_USAGE]: Could not create Usage item : query {query} : response {r.text} : {account['monday_account_id']}")
    logger.info(f'[MNDY_TOKEN_USAGE]: END : {account["monday_account_id"]}')
    return_success()

def return_success():
    return {
        'statusCode': 200,
        'body': json.dumps('Hello from Lambda!')
    }