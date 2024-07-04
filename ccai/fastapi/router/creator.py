from fastapi import APIRouter
from ccai.core.chatbots.creator import start_session, get_response, end_session

router = APIRouter(tags=["Creator"])

@router.get("/chat")
async def initiate_chat(creator_id: str, thread_id: str = None):
    response = await start_session(creator_id, thread_id)
    return response


@router.post("/chat")
async def run_query(creator_id: str, question: str):
    response = await get_response(creator_id, question)
    return response


@router.delete("/chat")
async def end_chat(creator_id: str):
    response = await end_session(creator_id)
    return response


@router.get("/")
async def test_endpoint():
    return "This is the creator router"
