import pinecone
import os
from pinecone import Pinecone
from pinecone import ServerlessSpec, PodSpec
import time

serverless = os.environ.get('USE_SERVERLESS','False').lower() == 'true'
use_serverless = True


''' Creating index '''

api_key = '765d993c-5d65-4a62-8021-7c140531c14d'
pc = Pinecone(api_key=api_key)

if use_serverless:
    spec = ServerlessSpec(cloud='aws',region='us-east-1')
else:
    spec = PodSpec(environment=environment)


index_name = "hello-pinecone"

if index_name in pc.list_indexes().names():
    pc.delete_index(index_name)
