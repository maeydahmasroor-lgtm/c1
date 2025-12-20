# backend/rag.py
import os
import asyncio
from dotenv import load_dotenv
from openai import AsyncOpenAI
from qdrant_client import AsyncQdrantClient

load_dotenv()

gemini_client = AsyncOpenAI(
    api_key=os.getenv("GEMINI_API_KEY"),
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"  # ✅ clean
)

qdrant_client = AsyncQdrantClient(path="./local_qdrant_v2")
COLLECTION_NAME = "book_rag"

async def query_rag(question: str, selected_text: str = None) -> str:
    if selected_text:
        return selected_text  # For testing: just echo selected text

    collections = await qdrant_client.get_collections()
    if not any(c.name == COLLECTION_NAME for c in collections.collections):
        return "❌ Collection missing. Run ingest.py."

    response = await gemini_client.embeddings.create(
        model="text-embedding-004",
        input=question
    )
    query_vector = response.data[0].embedding


    hits = await qdrant_client.search(
        collection_name=COLLECTION_NAME,
        query_vector=query_vector,
        limit=3
    )

    context = " ".join([
        hit.payload.get("text", "") for hit in hits
        if hit.payload and "text" in hit.payload
    ])

    if not context.strip():
        return "🔍 No context found."

    #response = await gemini_client.chat.completions.create(
    #    model="gemini-1.5-flash",
    #    messages=[{
    #        "role": "user",
    #        "content": f"Context: {context}\n\nQuestion: {question}\nAnswer in 1 sentence."
    #    }],
    #    temperature=0.0,
    #    max_tokens=100
    #)
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