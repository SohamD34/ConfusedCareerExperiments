from openai import OpenAI
from pinecone import Pinecone
import os
# from langchain_community.vectorstores import Pinecone
from langchain_community.embeddings.openai import OpenAIEmbeddings
from langchain_community.chat_models import ChatOpenAI
from langchain.chains import ConversationChain
from langchain.chains.conversation.memory import ConversationBufferWindowMemory
from langchain.prompts import SystemMessagePromptTemplate, HumanMessagePromptTemplate, ChatPromptTemplate, MessagesPlaceholder

os.environ['PINECONE_API_KEY'] = 'e147bfa7-e5f3-4fcf-ad1a-f25729052a4f'

class Chatbot:
    user_sessions = {}

    def __init__(self, chat_id, creator_id="asst_U2GM4YYl0atq60GfLRNxIZvr") -> None:
        
        openai_api_key = "sk-proj-6H9PJPDIdLrtAtoeCfVRT3BlbkFJiZ3V2AX9cWseafKMvoPj"

        self.client = OpenAI(api_key=openai_api_key)
        self.creator_id = creator_id
        self.chat_id = chat_id

        self.pc = Pinecone(api_key="e147bfa7-e5f3-4fcf-ad1a-f25729052a4f")
        self.index = self.pc.Index("confusedcareertest")

        # self.embedding = OpenAIEmbeddings(model="text-embedding-3-small", api_key="sk-proj-6H9PJPDIdLrtAtoeCfVRT3BlbkFJiZ3V2AX9cWseafKMvoPj")

        # self.embedding = OpenAIEmbeddings(model="text-embedding-3-small", api_key=openai_api_key)
        self.memory = ConversationBufferWindowMemory(k=3,return_messages=True)

        llm = ChatOpenAI(api_key=openai_api_key, model="gpt-3.5-turbo")

        system_msg_template = SystemMessagePromptTemplate.from_template(template="""Answer the question as truthfully as possible using the provided context, and if the answer is not contained within the text below, say 'I don't know'""")


        human_msg_template = HumanMessagePromptTemplate.from_template(template="{input}")

        prompt_template = ChatPromptTemplate.from_messages([system_msg_template, MessagesPlaceholder(variable_name="history"), human_msg_template])

        self.chain = ConversationChain(memory=self.memory, prompt=prompt_template, llm=llm, verbose=True)

        pass


    def load_bot(self):
        pass

    def pinecone_search(self, question):
        question_vec = self.client.embeddings.create(input=[question], model="text-embedding-3-small").data[0].embedding
        results = self.index.query(namespace=self.creator_id, vector=question_vec, top_k=3, include_values=False, include_metadata=True)

        context = []

        for r in results.matches:
            context.append(r.metadata['text'])

        return context

    async def run_chat(self, question):
        context = self.pinecone_search(question)

        # completion = self.client.chat.completions.create(
        #     model="gpt-3.5-turbo",
        #     messages=[
        #         {"role": "system", "content": "You are helpful assistant."},
        #         {"role": "user", "content": question}
        #     ]
        # )

        response = self.chain.predict(input=f"Question: {question}\nContext: {context}")

        return response


async def start_session(chat_id, creator_id):
    if chat_id in Chatbot.user_sessions:
        print("Session already started")
        return {'status': False, 'message': "Session already started"}

    instance = Chatbot(chat_id, creator_id)
    Chatbot.user_sessions[chat_id] = instance
    print("\nSession already started")
    return {'status': True, 'message': "Session started successfully"}
    

async def get_response(chat_id, question):
    print(Chatbot.user_sessions)
    if chat_id in Chatbot.user_sessions:
        response = await Chatbot.user_sessions[chat_id].run_chat(question)
        print("\nResponse received successfully")
        return {'status': True, 'message': response}

    print("\nFailed to get response")
    return {'status': False, 'message': 'Session not found'}


async def end_session(chat_id):
    if chat_id in Chatbot.user_sessions:
        del Chatbot.user_sessions[chat_id]
        print("\nSession ended successfully")
        return {'status': True, 'message': "Session ended successfully"}

    print("Failed to end session")
    return {'status': False, 'message': 'Session not found'}


if __name__ == "__main__":
    import asyncio

    async def test():
        print(await start_session("1", "test"))
        print(await get_response("1", "Hello. Give me some information on career in AI."))
        print(await end_session("1"))

    asyncio.run(test())
