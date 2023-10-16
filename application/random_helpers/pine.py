import pinecone
import os
from dotenv import load_dotenv
load_dotenv()

pinecone.init(api_key=os.getenv('PINECONE_API_KEY'), environment='us-east1-gcp')
index = pinecone.Index('obo-internal-slackbot')

def list_all_embeddings():
    stats = index.describe_index_stats()
    namespace_map = stats['namespaces']
    ret = []
    for namespace in namespace_map:
        if namespace == '7_Earnings':
            vector_count = namespace_map[namespace]['vector_count']
            res = index.query(vector=[0 for _ in range(1536)], top_k=10000, namespace=namespace, include_metadata=True)
            for match in res['matches']:
                doc_name = match['metadata']['file_name']
                print(doc_name)
                ret.append(match)
    return ret

def delete_all_vectors(namespace: str):
    index.delete(delete_all=True, namespace=namespace) 

# delete_all_vectors()
list_all_embeddings()
