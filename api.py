from fastapi import FastAPI
import uvicorn
from bot import start_session, get_response, end_session

import asyncio
from sse_starlette.sse import EventSourceResponse

from stream import Stream


app = FastAPI()


@app.put("/chat")
async def start_chat(data: dict):
    session_id = str(data.get("session_id", 0))

    response = start_session(session_id)

    return response


@app.post("/chat")
async def handle_chat(data: dict):
    message = data.get("message", "Default message if not found.")
    session_id = data.get("session_id", 0)
    session_id = str(session_id)

    stream = Stream(session_id)
    asyncio.create_task(get_response(stream, message, session_id))

    return EventSourceResponse(stream)


@app.delete("/chat")
async def end_chat(data: dict):
    session_id = data.get("session_id", 0)
    session_id = str(session_id)

    response = end_session(str(session_id))

    return response


@app.get("/test")
async def test_endpoint():
    return {"message": "This is a test endpoint for chatbot server."}


if __name__ == "__main__":
    uvicorn.run(app)
