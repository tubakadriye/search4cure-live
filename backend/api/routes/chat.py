from fastapi import APIRouter
from pydantic import BaseModel

from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.adk.memory import InMemoryMemoryService

from agent.agent import agent as root_agent


router = APIRouter()


# -------------------------
# Request model
# -------------------------

class ChatRequest(BaseModel):
    message: str
    session_id: str = "default"


# -------------------------
# Session + Memory
# -------------------------

session_service = InMemorySessionService()
memory_service = InMemoryMemoryService()


# -------------------------
# Runner
# -------------------------

runner = Runner(
    agent=root_agent,
    session_service=session_service,
    memory_service=memory_service,
    app_name="search4cure"
)


# -------------------------
# Chat endpoint
# -------------------------

@router.post("/chat")
async def chat(req: ChatRequest):

    result = await runner.run_async(
        input=req.message,
        session_id=req.session_id
    )

    return {
        "response": result.output_text
    }