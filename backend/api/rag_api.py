from fastapi import FastAPI
from backend.agent.agent import agent

app = FastAPI()

@app.post("/ask")
async def ask(query: str):

    response = await agent.run(query)

    return {"answer": response}