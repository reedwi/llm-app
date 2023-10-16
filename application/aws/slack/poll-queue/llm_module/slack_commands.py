from .obo_langchain import get_answer, get_personal_answer
from .obo_slack import get_thread_history, reply_in_thread, delete_slack_message
from .helpers import download_file, delete_local_file
from .supa import get_bucket, create_bucket, create_bucket_object, get_object_row_by_name_and_bucket, insert, update_by_id
from urllib.parse import quote


def yak(data, supabase):
    answer_obj = get_answer(namespace=data["namespace"], question=data["question"], chat_history=data["chat_history"], no_results=data["chatbot_message"])
    if answer_obj['chatgpt']:
        print(f'[SLACK_QUEUE_POLLER_YAK]: Replying to question in thread for ChatGPT question : {data["slack_team_id"]}')
        if data["thinking_ts"]:
            delete_slack_message(slack_key=data["slack_key"], channel_id=data["channel_id"], message_ts=data["thinking_ts"])
        reply = reply_in_thread(slack_key=data["slack_key"], channel_id=data["channel_id"], thread_ts=data["message_ts"], text=answer_obj['answer'])
    else:
        # TODO: Go through source documents
        if answer_obj['answer'].startswith("I'm sorry, but") and data["chatbot_message"] not in ['', None]:
            answer_obj['answer'] += f'\n{data["chatbot_message"]}'
        answer_obj['answer'] += '\n\n*Source(s)*'
        print(f'[SLACK_QUEUE_POLLER_YAK]: Getting sources for answer : {data["slack_team_id"]}')
        for i, document in enumerate(answer_obj['response']['source_documents'], start=1):
            supabase.postgrest.schema('storage')
            item = supabase.table('objects').select('*').eq('id', document.metadata['doc_id']).execute()
            try:
                doc_obj = item.data[0]
            except:
                doc_obj = None
                print(f'[SLACK_QUEUE_POLLER_YAK]: ERROR : Could not return document object from supabase : {data["slack_team_id"]}')

            if not doc_obj:
                continue
            supabase.postgrest.schema('public')
            
            item = supabase.table('documents').select('*').eq('document_object', document.metadata['doc_id']).execute()
            try:
                doc = item.data[0]
                do_not_include_source = doc['do_not_include_source']
            except:
                doc = None
                do_not_include_source = False
                print(f'[SLACK_QUEUE_POLLER_YAK]: ERROR : Could not return document from supabase : {data["slack_team_id"]}')
            try:
                if not do_not_include_source:
                    document_res = supabase.storage.get_bucket(doc_obj['bucket_id']).create_signed_url(path=doc_obj['name'], expires_in=3600, options={'download': False})
                    source_url = document_res['signedURL']
                    url_safe = quote(source_url, safe=':/?&=')
                    try:
                        url_safe += f'#page={document.metadata["page"]}'
                    except:
                        pass
                    answer_obj['answer'] += f'\n<{url_safe}|{doc_obj["path_tokens"][-1].split("_", 1)[1]}>'
                    try:
                        answer_obj['answer'] += f' ( Page {int(document.metadata["page"])})'
                    except:
                        pass
                else:
                    answer_obj['answer'] += f'\n{doc_obj["path_tokens"][-1].split("_", 1)[1]}'
            except:
                pass
            # print(document_res)
        print(f'[SLACK_QUEUE_POLLER_YAK]: Replying to question in thread for Custom Chatbot {data["namespace"]} question : {data["slack_team_id"]}')
        if data["thinking_ts"]:
            delete_slack_message(slack_key=data["slack_key"], channel_id=data["channel_id"], message_ts=data["thinking_ts"])
        reply = reply_in_thread(slack_key=data["slack_key"], channel_id=data["channel_id"], thread_ts=data["message_ts"], text=answer_obj['answer'])

    
    usage_obj = {
        'tokens_used': answer_obj['tokens_used'],
        'prompt': data["question"],
        'answer': answer_obj['answer'],
        'account_id': data['account_id'],
        'index_namespace': data["namespace"]
    }
    supabase.postgrest.schema('public')
    supabase.table('usage').insert(usage_obj).execute()
    
def yak_files(data, supabase):
    if data['original_question']:
        personal_chatbot = {
            'slack_user_id': data['user_id'],
            'thread_ts': data['message_ts'],
            'account_id': data['account_id'],
            'channel_id': data['channel_id']
        }
        supabase.postgrest.schema('public')
        personal_bot = supabase.table('personal_chatbots').insert(personal_chatbot).execute()
        try:
            personal_bot_id = personal_bot.data[0]['id']
        except:
            personal_bot_id = None
            print(f'SLACK_QUEUE_POLLER_YAK_FILES: ERROR : Could not create personal chatbot row : {personal_chatbot}')

        try:
            files = data['chat_history'][1]['files']
        except:
            print('SLACK_QUEUE_POLLER_YAK_FILES: ERROR : No files to process for personal chatbot')
        
        for file in files:
            bucket = get_bucket(supabase=supabase, bucket_name=data['user_id'])
            print(f'FILE CONTENT: {file}')
            if not bucket:
                bucket = create_bucket(supabase=supabase, bucket_name=data['user_id'])
                print(f'[SLACK_QUEUE_POLLER_YAK_FILES]: Created bucket: {bucket} : {data["account_id"]} : {data["user_id"]}')
            
            supa_file_path = f'{data["user_id"]}/{data["message_ts"]}/{file["name"]}'
            local_file_path = f'/tmp/{file["name"]}'
            print(f'[SLACK_QUEUE_POLLER_YAK_FILES]: Downloading file locally {local_file_path}  : {data["account_id"]} : {data["user_id"]}')
            local_file_object = download_file(
                url=file["url_private_download"],
                local_filename=local_file_path,
                access_token=data['slack_key']
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
            file_content_type = content_type.get(file["filetype"], file["mimetype"])
            print(f'[SLACK_QUEUE_POLLER_YAK_FILES]: Uploading file to Supabase {local_file_path}  : {data["account_id"]} : {data["user_id"]}')
            supa_file_object = create_bucket_object(
                supabase=supabase,
                bucket_name=data["user_id"],
                path=supa_file_path,
                file_contents=local_file_object,
                file_content_type=file_content_type
            )
            
            print(f'[SLACK_QUEUE_POLLER_YAK_FILES]: Deleting file locally {local_file_path}  : {data["account_id"]} : {data["user_id"]}')
            delete_local_file(local_file_path)

            supa_storage_row = get_object_row_by_name_and_bucket(
                supabase=supabase,
                bucket_id=data["user_id"],
                path=supa_file_path
            )

            document = {
                'document_name': file["name"],
                'document_type': file["filetype"],
                'bucket_location': data["user_id"],
                'document_object': supa_storage_row['id'],
                'account_id': data["account_id"],
                'file_name': file["name"],
                'file_status': 'INSERT',
                'personal_chatbot_id': personal_bot_id,
            }
            document_row = insert(supabase=supabase, table_name='documents', data=document)
            print(f'[SLACK_QUEUE_POLLER_YAK_FILES]: Document {file["name"]} inserted into the database : {data["account_id"]} : {data["user_id"]}')
        update_by_id(supabase=supabase, table_name='personal_chatbots', id=personal_bot_id, data={"status": 'READY'})
    else:
        chat_history = data['chat_history'][3:]
        if len(chat_history) <= 1:
            chat_history = None
        answer_obj = get_personal_answer(namespace=data['namespace'], question=data['question'], chat_history=chat_history)
        answer_obj['answer'] += '\n\n*Source(s)*'
        print(f'[SLACK_QUEUE_POLLER_YAK_FILES]: Getting sources for answer : {data["slack_team_id"]}')
        for i, document in enumerate(answer_obj['response']['source_documents'], start=1):
            print(document)
            supabase.postgrest.schema('storage')
            item = supabase.table('objects').select('*').eq('id', document.metadata['doc_id']).execute()
            try:
                doc_obj = item.data[0]
            except:
                doc_obj = None
                print(f'[SLACK_QUEUE_POLLER_YAK_FILES]: ERROR : Could not return document object from supabase : {data["slack_team_id"]}')

            if not doc_obj:
                continue
            try:
                document_res = supabase.storage.get_bucket(doc_obj['bucket_id']).create_signed_url(path=doc_obj['name'], expires_in=3600, options={'download': False})
                source_url = document_res['signedURL']
                url_safe = quote(source_url, safe=':/?&=')
                try:
                    url_safe += f'#page={document.metadata["page"]}'
                except:
                    pass
                answer_obj['answer'] += f'\n<{url_safe}|{document.metadata["file_name"]}>'
                try:
                    answer_obj['answer'] += f' ( Page {int(document.metadata["page"])})'
                except:
                    pass
            except:
                print('outside try')
                pass
            # print(document_res)
        print(f'[SLACK_QUEUE_POLLER_YAK_FILES]: Replying to question in thread for Custom Chatbot {data["namespace"]} question : {data["slack_team_id"]}')
        if data["thinking_ts"]:
            delete_slack_message(slack_key=data["slack_key"], channel_id=data["channel_id"], message_ts=data["thinking_ts"])
        reply = reply_in_thread(slack_key=data["slack_key"], channel_id=data["channel_id"], thread_ts=data["message_ts"], text=answer_obj['answer'])
        usage_obj = {
            'tokens_used': answer_obj['tokens_used'],
            'prompt': data["question"],
            'answer': answer_obj['answer'],
            'account_id': data['account_id'],
            'index_namespace': data["namespace"]
        }
        supabase.postgrest.schema('public')
        supabase.table('usage').insert(usage_obj).execute()

        

    