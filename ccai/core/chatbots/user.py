from openai import OpenAI
import time


class Chatbot:
    user_sessions = {}

    def __init__(self, chat_id, creator_id="asst_U2GM4YYl0atq60GfLRNxIZvr") -> None:
        self.client = OpenAI(api_key="sk-proj-6H9PJPDIdLrtAtoeCfVRT3BlbkFJiZ3V2AX9cWseafKMvoPj")
        self.creator_id = creator_id
        self.chat_id = chat_id
        pass


    def load_bot(self):
        pass


    async def run_chat(self, question):
        # print(question)
        completion = self.client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are helpful assistant."},
                {"role": "user", "content": question}
            ]
        )
        return completion.choices[0].message



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
        print(await start_session("1", "1"))
        print(await get_response("1", "Hello. Give me some information on career in AI."))
        print(await end_session("1"))

    asyncio.run(test())