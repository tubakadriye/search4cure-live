from fastapi import FastAPI
from backend.api.routes.chat import router as chat_router

app = FastAPI(title="Search4Cure API")

app.include_router(chat_router)