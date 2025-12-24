import google.generativeai as genai
import os
from qdrant_client import AsyncQdrantClient

# -----------------------------
# Qdrant Cloud
# -----------------------------
qdrant_client = AsyncQdrantClient(
    url=os.getenv("QDRANT_URL2"),
    api_key=os.getenv("QDRANT_API_KEY2")
)

collection_name = "rag2"

# ----------

# -----------------------------
# RAG Query
# -----------------------------
async def query_rag(question: str, selected_text: str | None = None) -> str:

    response = gemini_client.embeddings.create(
        model="text-embedding-004",
        input=question
    )
    query_vector = response.data[0].embedding

    hits = await client.query_points(
        collection_name=collection_name,
        query=response,
        limit=5
    )

    context = "\n\n".join(p.payload["text"] for p in hits.points)

    if selected_text:
        context = selected_text + "\n\n" + context

    genai.configure(api_key=os.getenv("GEMINI_API_KEY3"))
    model = genai.GenerativeModel("gemma-3-27b-it")

    prompt = f"""
You are a helpful book assistant.

Context:
{context}

Question:
{question}

Answer:
"""

    return model.generate_content(prompt).text
