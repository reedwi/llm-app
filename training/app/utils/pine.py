import pinecone
import os
from dotenv import load_dotenv
load_dotenv()

pinecone.init(api_key=os.getenv('PINECONE_API_KEY'), environment='us-east1-gcp')
index = pinecone.Index('obo-internal-slackbot')


def delete_vectors(namespace: str, document_id: int):
    index.delete(
        namespace=namespace,
        filter={
            "doc_id": document_id
        }
    )

def delete_all_vectors(namespace: str):
    index.delete(delete_all=True, namespace=namespace) 