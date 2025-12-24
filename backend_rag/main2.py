from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional
from rag import query_rag

app = FastAPI(title="Book RAG API")

# DEV CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

class AskRequest(BaseModel):
    question: str
    selected_text: Optional[str] = None

@app.post("/query/selected-text")
def ask(req: AskRequest):
    try:
        answer = query_rag(req.question, req.selected_text)
        return {"answer": answer}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/")
def health():
    return {"status": "✅ Backend running"}
