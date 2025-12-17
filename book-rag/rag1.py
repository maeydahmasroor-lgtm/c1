# backend/rag.py
import os
import asyncio
from dotenv import load_dotenv
from openai import AsyncOpenAI
from qdrant_client import QdrantClient
from qdrant_client.models import VectorParams, Distance

load_dotenv()

# 🔑 Initialize clients
gemini_client = AsyncOpenAI(
    api_key=os.getenv("GEMINI_API_KEY"),
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"  # ✅ no trailing spaces!
)

# ✅ LOCAL QDRANT (no network issues)
qdrant_client = QdrantClient(path="./local_qdrant")  # ← data stored in ./local_qdrant

COLLECTION_NAME = "rag2"

async def embed_text(text: str) -> list[float]:
    """Embed text using Gemini's text-embedding-004 (768-dim)"""
    response = await gemini_client.embeddings.create(
        model="text-embedding-004",
        input=text
    )
    return response.data[0].embedding

async def query_rag(question: str, selected_text: str = None) -> str:
    # 🔍 Retrieve context
    if selected_text:
        context = selected_text
    else:
        # 1. Embed query
        query_vector = await embed_text(question)
        
        # 2. Search local Qdrant
        hits = qdrant_client.search(
            collection_name=COLLECTION_NAME,
            query_vector=query_vector,
            limit=4
        )
        
        # 3. Build context
        context_parts = []
        for hit in hits:
            chapter = hit.payload.get("chapter", "Unknown")
            text = hit.payload.get("text", "")
            context_parts.append(f"[{chapter}]: {text}")
        context = "\n\n---\n\n".join(context_parts)

    # 🧠 Generate answer
    response = await gemini_client.chat.completions.create(
        model="gemini-1.5-flash",
        messages=[
            {
                "role": "system",
                "content": (
                    "You are a helpful assistant for a technical book. "
                    "Answer using ONLY the context below. If unsure, say 'Not covered in the book.'"
                )
            },
            {
                "role": "user",
                "content": f"Context:\n{context}\n\nQuestion: {question}"
            }
        ],
        temperature=0.3,
        max_tokens=500
    )
    return response.choices[0].message.content