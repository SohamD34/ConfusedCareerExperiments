from pinecone.grpc import PineconeGRPC as Pinecone
from pinecone import ServerlessSpec
from langchain.embeddings.openai import OpenAIEmbeddings

''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
'    UNDER EXPERIMENTATION -  DO NOT TEST                    '
''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''

openai_api_key = 'sk-proj-6H9PJPDIdLrtAtoeCfVRT3BlbkFJiZ3V2AX9cWseafKMvoPj'
model_name = 'text-embedding-3-small'

pc = Pinecone(api_key="e147bfa7-e5f3-4fcf-ad1a-f25729052a4f")


# Activating pre-existing serverless index 

index_name = "confusedcareertest"

embedding = OpenAIEmbeddings()

index = pc.from_documents(index_name)
print(index)