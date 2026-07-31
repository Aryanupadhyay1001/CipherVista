from fastapi import FastAPI

from src.api.routes import router

app = FastAPI(
    title="CipherVista API",
    version="1.0.0"
)

app.include_router(router)

@app.get("/")
def home():
    return {
        "message": "CipherVista API Running"
    }