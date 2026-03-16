from fastapi import FastAPI
from backend.api.routes.chat import router as chat_router

app = FastAPI(title="Search4Cure API")

# Include your chat router
app.include_router(chat_router, prefix="/api")

# Optional: Root endpoint to avoid 404
@app.get("/")
def root():
    return {"message": "Search4Cure API is running!"}