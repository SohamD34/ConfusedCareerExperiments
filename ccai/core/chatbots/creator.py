from openai import OpenAI
from pinecone import Pinecone
import time


class Chatbot:
    sessions = {}

    def __init__(self, creator_id) -> None:
        self.client = OpenAI(api_key="sk-proj-6H9PJPDIdLrtAtoeCfVRT3BlbkFJiZ3V2AX9cWseafKMvoPj")
        self.assistant_id = "asst_U2GM4YYl0atq60GfLRNxIZvr"
        self.creator_id = creator_id
        self.thread_id = None

        self.pc = Pinecone(api_key="e147bfa7-e5f3-4fcf-ad1a-f25729052a4f")
        self.index = self.pc.Index("confusedcareertest")

        self.messages = []

        pass

    async def create_new_thread(self):
        thread = self.client.beta.threads.create(messages=[])
        self.thread_id = thread.id

        return self.thread_id

    async def load_thread(self, thread_id):
        self.thread_id = thread_id

        return self.thread_id

    def poll_run(self, run):
        while run.status != "completed":
            run = self.client.beta.threads.runs.retrieve(
                thread_id=self.thread_id,
                run_id=run.id,
            )
            time.sleep(0.5)
        return run

    async def run_chat(self, question):
        # self.client.beta.threads.messages.create(thread_id=self.thread_id, role="user", content=question)
        # with self.client.beta.threads.runs.stream(thread_id=self.thread_id, assistant_id=self.assistant_id, event_handler=EventHandler(), temperature=0) as stream:
        #     stream.until_done()
        self.client.beta.threads.messages.create(thread_id=self.thread_id, role="user", content=question)
        run = self.client.beta.threads.runs.create(thread_id=self.thread_id, assistant_id=self.assistant_id)
        run = self.poll_run(run)

        print(run.usage)

        messages = self.client.beta.threads.messages.list(thread_id=self.thread_id, order="desc", limit=1)

        for m in messages:
            answer = m.content[0].text.value
            break

        self.messages.append({"role": "user", "content": question})
        self.messages.append({"role": "assistant", "content": answer})

        return answer
    
    async def upsert_messages(self):
        inputs = []
        values = []
        for i in range(0, len(self.messages), 2):
            question = self.messages[i]["content"]
            answer = self.messages[i+1]["content"]

            text = "Question: " + question + "\nAnswer: " + answer + "\n"
            inputs.append(text)
            values.append(self.client.embeddings.create(input=[text], model="text-embedding-3-small").data[0].embedding)

        vectors = [{"id": str(i), "values": v, "metadata": {"text": inputs[i]}} for i, v in enumerate(values)]
        self.index.upsert(vectors, namespace=self.creator_id)

        return self.index.describe_index_stats()


async def start_session(creator_id, thread_id):
    if creator_id in Chatbot.sessions:
        # print("Session already started")
        return {'status': False, 'message': "Session already started"}

    instance = Chatbot(creator_id)
    if not thread_id:
        thread_id = await instance.create_new_thread()
        Chatbot.sessions[creator_id] = instance
        return {'status': True, 'message': "Session started successfully", 'thread_id': thread_id}
    else:
        thread_id = await instance.load_thread(thread_id)
        Chatbot.sessions[creator_id] = instance
        return {'status': True, 'message': "Session started successfully", 'thread_id': thread_id}


async def get_response(creator_id, question):
    # print(Chatbot.sessions)
    if creator_id in Chatbot.sessions:
        response = await Chatbot.sessions[creator_id].run_chat(question)
        # print("Response received successfully")
        return {'status': True, 'message': response}

    print("Failed to get response")
    return {'status': False, 'message': 'Session not found'}


async def end_session(creator_id):
    if creator_id in Chatbot.sessions:
        instance = Chatbot.sessions[creator_id]
        response = await instance.upsert_messages()

        del Chatbot.sessions[creator_id]
        # print("Session ended successfully")
        return {'status': True, 'message': "Session ended successfully", 'response': response}

    # print("Failed to end session")
    return {'status': False, 'message': 'Session not found'}


if __name__ == "__main__":
    import asyncio

    async def test():
        print(await start_session("test", None))
        await get_response("test", "Hello. Give me some information on career in AI.")
        await get_response("test", "I am thinking about pursuing a PhD")
        # await get_response("test", "My end goal is to get a senior research scientist position in a top tech company. What should I do?")

        print(await end_session("test"))

    asyncio.run(test())