from fastapi import APIRouter
from ccai.core.chatbots.user import start_session, get_response, end_session

router = APIRouter(tags=["User"])

@router.get("/chat")
async def initiate_chat(user_id: str, thread_id: str = None):
    response = await start_session(user_id, thread_id)
    return response


@router.post("/chat")
async def run_query(user_id: str, question: str):
    response = await get_response(user_id, question)
    return response


@router.delete("/chat")
async def end_chat(user_id: str):
    response = await end_session(user_id)
    return response


@router.get("/")
async def test_endpoint():
    return "This is the user router"
