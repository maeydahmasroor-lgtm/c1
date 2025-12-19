# backend/rag.py
import os
import asyncio
from dotenv import load_dotenv
from openai import AsyncOpenAI
from qdrant_client import AsyncQdrantClient

load_dotenv()

# ✅ FIXED: NO TRAILING SPACES
gemini_client = AsyncOpenAI(
    api_key=os.getenv("GEMINI_API_KEY"),
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"  # ← clean
)

qdrant_client = AsyncQdrantClient(path="./local_qdrant")
COLLECTION_NAME = "rag4"

async def embed_text(text: str) -> list[float]:
    # ✅ Use text-embedding-004 (Gemini's model)
    response = await gemini_client.embeddings.create(
        model="text-embedding-004",  # ← correct model
        input=text
    )
    return response.data[0].embedding

async def query_rag(question: str, selected_text: str = None) -> str:
    if selected_text:
        context = selected_text
    else:
        # Check collection exists (prevent 500)
        collections = await qdrant_client.get_collections()
        if not any(c.name == COLLECTION_NAME for c in collections.collections):
            return "❌ Knowledge base not loaded. Run `ingest.py` first."

        query_vector = await embed_text(question)
        hits = await qdrant_client.search(
            collection_name=COLLECTION_NAME,
            query_vector=query_vector,
            limit=3
        )
        
        # Safely extract text
        context = "\n\n---\n\n".join([
            hit.payload.get("text", "").strip()
            for hit in hits
            if hit.payload and hit.payload.get("text")
        ])

        if not context.strip():
            return "🔍 No relevant content found in the book."

    # Generate answer
    response = await gemini_client.chat.completions.create(
        model="gemini-1.5-flash",
        messages=[
            {"role": "user", "content": f"Book context:\n{context}\n\nQuestion: {question}\nAnswer concisely using only the context."}
        ],
        temperature=0.2,
        max_tokens=300
    )
    return response.choices[0].message.content.strip()