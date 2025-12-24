# app/main.py
import os
from fastapi import FastAPI
from pydantic import BaseModel
from qdrant_client import QdrantClient
import genai
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List

app = FastAPI(title="Book RAG API")
# ---------------------------
# Load secrets (use env variables or .env)
# ---------------------------
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")
QDRANT_URL = os.environ.get("QDRANT_URL")
QDRANT_API_KEY = os.environ.get("QDRANT_API_KEY")
QDRANT_COLLECTION = os.environ.get("QDRANT_COLLECTION")
# DEV CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
# ---------------------------
# Initialize clients
# ---------------------------
qdrant = QdrantClient(
    url=QDRANT_URL,
    api_key=QDRANT_API_KEY
)

genai_client = genai.Client(api_key=GEMINI_API_KEY)
#genai.configure(api_key=GEMINI_API_KEY)

#model = genai.GenerativeModel("gemini-1.5-flash")
#response = model.generate_content("Hello!")
# ---------------------------
# FastAPI app
# ---------------------------
app = FastAPI(title="Book Chatbot API")

# ---------------------------
# Request & Response Models
# ---------------------------
class QuestionRequest(BaseModel):
    question: str

class AnswerResponse(BaseModel):
    answer: str
    sources: List[str]

# ---------------------------
# Retriever (No embeddings)
# ---------------------------
def retriever_agent(question: str):
    hits, _ = qdrant.scroll(
        collection_name="rag2",
        limit=10
    )

    matched = []
    for point in hits:
        text = point.payload.get("text", "")
        if any(word.lower() in text.lower() for word in question.split()):
            matched.append(point.payload)

    return matched[:3]

# ---------------------------
# Gemini LLM
# ---------------------------
def llm_agent(question: str, context_blocks):
    if not context_blocks:
        return "The book does not contain this information."

    context = "\n\n".join(c["text"] for c in context_blocks)

    prompt = f"""
You are an academic book assistant.

Rules:
- Answer strictly from the provided book content
- If the answer is not present, say:
  "The book does not contain this information."

Book Content:
{context}

Question:
{question}
"""
    
    model = genai.GenerativeModel("gemini-1.5-flash")
    response = model.generate_content(
        contents=prompt
    )

    return response.text

# ---------------------------
# API endpoint
# ---------------------------
@app.post("/ask", response_model=AnswerResponse)
async def ask_question(req: QuestionRequest):
    context_blocks = retriever_agent(req.question)
    answer = llm_agent(req.question, context_blocks)
    sources = list({c.get("chapter_title", "Unknown") for c in context_blocks})
    return AnswerResponse(answer=answer, sources=sources)
