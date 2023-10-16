from pathlib import Path
import os
from langchain.chat_models import ChatOpenAI
from langchain.agents import Tool
from langchain.chains.conversation.memory import ConversationBufferWindowMemory
from langchain.agents import initialize_agent
from langchain.vectorstores import Pinecone
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.document_loaders import TextLoader, PyPDFLoader, Docx2txtLoader
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.chains import RetrievalQAWithSourcesChain, RetrievalQA
from langchain import OpenAI
import pinecone
from dotenv import load_dotenv
load_dotenv()

pinecone.init(api_key=os.getenv('PINECONE_API_KEY'),
              environment="us-east1-gcp")

def load_and_split_txt(file_path: str, namespace: str, file_name: str, doc_id: str):
    loader = TextLoader(file_path)
    docs = loader.load()
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
    split_docs = text_splitter.split_documents(docs)
    for doc in split_docs:
        doc.metadata['namespace'] = namespace
        doc.metadata['file_name'] = file_name
        doc.metadata['doc_id'] = doc_id

    return split_docs

def create_pinecone_index(documents: list, namespace: str):
    '''namespace is monday_account_id'''
    embeddings = OpenAIEmbeddings()
    vector_db = Pinecone.from_documents(documents=documents, embedding=embeddings, index_name='obo-internal-slackbot', namespace=namespace)
    return vector_db

def main():
    pi_index = pinecone.Index('obo-internal-slackbot')
    pi_index.delete(delete_all=True, namespace="6595839_HR") 
    chunks = []
    hb_file = './documents/handbook.txt'
    namespace = '6595839_HR'
    hb_file_name = 'handbook.txt'
    hb_doc_id = 'c2dd2904-589a-474f-b518-855ddee174d2'
    hb_docs = load_and_split_txt(file_path=hb_file, namespace=namespace, file_name=hb_file_name, doc_id=hb_doc_id)
    chunks.extend(hb_docs)

    cal_file = './documents/calendar.txt'
    cal_file_name = 'calendar.txt'
    cal_doc_id = 'c61dd3c3-4738-4498-a933-9166e61cd484'
    cal_docs = load_and_split_txt(file_path=cal_file, namespace=namespace, file_name=cal_file_name, doc_id=cal_doc_id)
    chunks.extend(cal_docs)

    vector_db = create_pinecone_index(documents=chunks, namespace=namespace)

if __name__ == '__main__':
    main()