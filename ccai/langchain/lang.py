import langchain
import langchain_community
from langchain_openai import OpenAIEmbeddings
from pinecone import Pinecone

''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
'    UNDER EXPERIMENTATION -  DO NOT TEST                    '
''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''


openai_api_key = 'sk-proj-6H9PJPDIdLrtAtoeCfVRT3BlbkFJiZ3V2AX9cWseafKMvoPj'
model_name = 'text-embedding-3-small'

pc = Pinecone(api_key="e147bfa7-e5f3-4fcf-ad1a-f25729052a4f")

embed = OpenAIEmbeddings(
    model=model_name,
    openai_api_key=openai_api_key
)

text_field = "text"
index_name = "confusedcareertest"
index = pc.Index(index_name)

# print(index.describe_index_stats())     # Describes dimension & total vector count