"""
FastAPI backend for Physical AI Textbook RAG Chatbot
"""
import os
from dotenv import load_dotenv
load_dotenv()

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List

# Import RAG engine (ensure rag.py is in same directory)
from rag5 import RAGEngine

app = FastAPI(
    title="Physical AI Textbook API",
    description="RAG-powered Q&A for robotics education (Gemini)",
    version="2.0.0"
)

# ✅ FIXED: Clean CORS origins (no trailing spaces)
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "https://physical-ai-humanoid-robotics-with.vercel.app"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Models
class AskRequest(BaseModel):
    question: str

class AskSelectionRequest(BaseModel):
    question: str
    selection: str

class AskResponse(BaseModel):
    answer: str
    sources: List[dict] = []

# Endpoints
@app.get("/")
async def root():
    return {
        "message": "Physical AI Textbook API (Gemini)",
        "docs": "/docs", 
        "health": "/api/health"
    }

@app.get("/api/health")
async def health_check():
    return {
        "status": "ok", 
        "service": "physical-ai-textbook-api",
        "collection": "physical_ai_book"
    }

@app.post("/query/selected-text", response_model=AskResponse)
async def ask_question(request: AskRequest):
    """RAG Q&A on full textbook content"""
    try:
        rag = RAGEngine()
        result = await rag.ask(request.question)
        return AskResponse(
            answer=result["answer"],
            sources=result.get("sources", [])
        )
    except Exception as e:
        print(f"❌ ASK ERROR: {e}")  # Visible in logs
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/ask-selection", response_model=AskResponse)
async def ask_about_selection(request: AskSelectionRequest):
    """Q&A about selected text"""
    try:
        rag = RAGEngine()
        result = await rag.ask_selection(
            question=request.question,
            selection=request.selection
        )
        return AskResponse(answer=result["answer"])
    except Exception as e:
        print(f"❌ SELECTION ERROR: {e}")
        raise HTTPException(status_code=500, detail=str(e))