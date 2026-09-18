# Agentic GraphRAG

A starter project for an agentic GraphRAG system combining vector search, knowledge-graph search, and an orchestration agent.

## Structure
- `backend/` FastAPI backend and RAG/graph/agent logic
- `data/raw/` source documents
- `data/processed/` extracted/cleaned data
- `frontend/` dashboard starter
- `.env.example` environment-variable template

## Run backend
```bash
python -m venv .venv
# Windows: .venv\Scripts\activate
pip install -r requirements.txt
uvicorn backend.main:app --reload
```

## API
- `GET /` health check
- `POST /search` starter search endpoint

Configure credentials in `.env` before connecting real LLM, embedding, or TigerGraph services.
