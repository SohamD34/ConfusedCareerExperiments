from openai import OpenAI
from typing_extensions import override
from openai import AssistantEventHandler
import time

from stream_model import BaseStreamingMessage, StreamingStartMessage, StreamingTokenMessage, StreamingEndMessage

client = OpenAI(api_key="sk-proj-6H9PJPDIdLrtAtoeCfVRT3BlbkFJiZ3V2AX9cWseafKMvoPj")
ASSISTANT_ID="asst_Lzs2hBGKqqasld9K98qwir2K"


class EventHandler(AssistantEventHandler):
    @override
    def on_text_created(self, text) -> None:
        # print("Hello")
        print(f"\nassistant > ", end="", flush=True)
        # await self.stream_self.asend(StreamingTokenMessage(message="assistant >"))

    @override
    def on_text_delta(self, delta, snapshot):
        # print("Hello2")
        print(delta.value, end="", flush=True)
        # await self.stream_self.asend(StreamingTokenMessage(message=delta.value))

    def on_tool_call_created(self, tool_call):
        # print("Hello3")
        print(f"\nassistant > {tool_call.type}\n", flush=True)
        # await self.stream_self.asend(StreamingTokenMessage(message=f"assistant > {tool_call.type}"))

    def on_tool_call_delta(self, delta, snapshot):
        # print("Hello4")
        if delta.type == 'code_interpreter':
            if delta.code_interpreter.input:
                print(delta.code_interpreter.input, end="", flush=True)
                # await self.stream_self.asend(StreamingTokenMessage(message=delta.code_interpreter.input))

            if delta.code_interpreter.outputs:
                print(f"\n\noutput >", flush=True)
                # await self.stream_self.asend(StreamingTokenMessage(message="output >"))

                for output in delta.code_interpreter.outputs:
                    if output.type == "logs":
                        print(f"\n{output.logs}", flush=True)
                        # await self.stream_self.asend(StreamingTokenMessage(message=output.logs))


class Chatbot:
    sessions = {}

    def __init__(self) -> None:
        pass


def start_session(session_id):
    thread = client.beta.threads.create(messages=[])
    thread_id = thread.id

    Chatbot.sessions[session_id] = thread_id

    print("Session started successfully")
    return {'status': True, 'message': "Session started successfully"}


async def get_response(stream_self, question, session_id):
    if session_id in Chatbot.sessions:

        # await stream_self.asend(StreamingStartMessage())

        thread_id = Chatbot.sessions[session_id]
        client.beta.threads.messages.create(thread_id=thread_id, role="user", content=question)
        with client.beta.threads.runs.stream(thread_id=thread_id, assistant_id=ASSISTANT_ID, event_handler=EventHandler(), temperature=0) as stream:
            stream.until_done()

        await stream_self.asend(StreamingEndMessage())

        return {'status': True, 'response': "Response received"}
    else:
        return {'status': False, 'message': 'Session not found'}


def end_session(session_id):
    if session_id in Chatbot.sessions:
        del Chatbot.sessions[session_id]
        print("Session ended successfully")
        return {'status': True, 'message': 'Session ended successfully'}

    print("Failed to end session")
    return {'status': False, 'message': 'Session not found'}


if __name__ == "__main__":
    start_session("1")
    get_response("1", "Should I go for a PhD or get a job?")

    time.sleep(5)

    get_response("1", "I have interest in AI and my long term goal is to a senior researcher in a good firm")

    end_session("1")