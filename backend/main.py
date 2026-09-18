from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI(title="Agentic GraphRAG API", version="0.1.0")

class SearchRequest(BaseModel):
    query: str

@app.get("/")
def health():
    return {"status": "ok", "service": "agentic-graphrag"}

@app.post("/search")
def search(request: SearchRequest):
    return {
        "query": request.query,
        "message": "Connect vector/graph tools in backend/agent/orchestrator.py"
    }
