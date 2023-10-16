import os
from dotenv import load_dotenv
load_dotenv()
from supabase import client, create_client

supabase: client = create_client(os.getenv('SUPABASE_URL'), os.getenv('SUPABASE_KEY'))

def empty_bucket(supabase, bucket_id: str):
    supabase.storage.empty_bucket(bucket_id)
    try:
        supabase.storage.empty_bucket(bucket_id)
    except:
        print(f'Error emptying bucket: {bucket_id}')

def delete_bucket(supabase, bucket_id: str):
    try:
        supabase.storage.delete_bucket(bucket_id)
    except:
        print(f'Error deleting bucket: {bucket_id}')

def get_bucket(supabase, bucket_name: str):
    try:
        bucket = supabase.storage.get_bucket(id=bucket_name)
        return bucket
    except:
        print(f'Bucket: {bucket_name} does not exist')
        return None

bucket = get_bucket(supabase=supabase, bucket_name='7362006')
print(bucket.list('testdsing'))
for file in bucket.list('testdsing'):
    bucket.remove([f"testdsing/{file['name']}"])
# empty_bucket(supabase=supabase, bucket_id='7362006/testdsing')