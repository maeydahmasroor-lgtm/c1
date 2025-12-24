# backend/main.py
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from rag import query_rag
from fastapi.middleware.cors import CORSMiddleware
from typing import Optional
app = FastAPI(title="Book RAG API")

# Allow Docusaurus frontend (adjust for prod)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class AskRequest(BaseModel):
    question: str
    selected_text: Optional[str] = None

@app.post("/query/selected-text")
async def ask(req: AskRequest):
    try:
        answer = await query_rag(req.question, req.selected_text)
        return {"answer": answer}
    except Exception as e:
        raise HTTPException(500, f"RAG error: {str(e)}")

# Health check
@app.get("/")
def health():
    return {"status": "✅ RAG backend is running!"}