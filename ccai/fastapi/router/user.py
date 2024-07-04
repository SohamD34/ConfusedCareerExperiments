from fastapi import APIRouter

router = APIRouter(tags=["User"])

@router.get("/chat")
async def initiate_chat():
    return "This is the user initiate chat"


@router.post("/chat")
async def get_response():
    return "This is the user chat response endpoint."


@router.delete("/chat")
async def end_chat():
    return "This is the user end chat endpoint"


@router.get("/")
async def test_endpoint():
    return "This is the user router"
