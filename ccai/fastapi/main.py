from fastapi import FastAPI

from ccai.fastapi.router import router as creator_router
from ccai.fastapi.router import router as user_router


app = FastAPI(title="Confused Career AI Core")

app.include_router(creator_router, prefix="/creator")
app.include_router(user_router, prefix="/user")


@app.get("/", tags=["Root"])
def root():
    """Root endpoint"""
    return {
        "success": True,
        "message": "Welcome to ConfusedCareers!",
    }
