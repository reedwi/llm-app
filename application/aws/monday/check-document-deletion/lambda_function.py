import json
import os
from supabase import client, create_client
import lib.supa as supa
import logging

supabase: client = create_client(os.getenv('SUPABASE_URL'), os.getenv('SUPABASE_KEY'))
logger = logging.getLogger()
logger.setLevel(logging.INFO) 

def lambda_handler(event, context):
   logger.info('[MNDY_CHECK_DOCUMENT_DELETION]: ENTER')
   body = json.loads(event['body'])
   asset_ids = body['asset_ids']
   chatbot_id = body['chatbot_id']
   logger.info(f'[MNDY_CHECK_DOCUMENT_DELETION]: START : Chatbot ID {chatbot_id}')
   documents = supa.get_by_dynamic_col(supabase=supabase, table_name='documents', column_name='chatbot_id', column_value=chatbot_id)
   supabase_asset_ids = [doc['id'] for doc in documents]
   missing_asset_ids = list(set(supabase_asset_ids) - set(asset_ids))
   delete = False
   logger.info(f'[MNDY_CHECK_DOCUMENT_DELETION]: Preparing {len(missing_asset_ids)} documents for deletion')
   for asset_id in missing_asset_ids:
      delete = True
      data = {
         'file_status': 'DELETE'
      }
      supa.update_by_id(supabase=supabase, table_name='documents', id=asset_id, data=data)
   logger.info(f'[MNDY_CHECK_DOCUMENT_DELETION]: END : Chatbot ID {chatbot_id}')
   return {
      'statusCode': 200,
      'body': json.dumps({"delete": delete})
   }