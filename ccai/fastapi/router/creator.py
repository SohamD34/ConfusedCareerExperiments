from fastapi import APIRouter

router = APIRouter(tags=["Creator"])

@router.get("/chat")
async def initiate_chat():
    return "This is the creator initiate chat endpoint"


@router.post("/chat")
async def get_response():
    return "This is the creator chat response endpoint."


@router.delete("/chat")
async def end_chat():
    return "This is the creator end chat endpoint"


@router.get("/")
async def test_endpoint():
    return "This is the creator router"

