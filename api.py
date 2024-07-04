import ccai

from fastapi import FastAPI

from ccai.fastapi.router.creator import router as creator_router
from ccai.fastapi.router.user import router as user_router


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

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="localhost", port=8000)
