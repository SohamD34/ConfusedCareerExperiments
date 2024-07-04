from fastapi import APIRouter

router = APIRouter(tags=["User"])

@router.get("/chat")
async def initiate_chat():
    return "This is the creator initiate chat"


@router.get("/")
async def test_endpoint():
    return "This is the user router"
