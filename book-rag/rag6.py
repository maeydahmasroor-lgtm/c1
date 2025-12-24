# backend/rag6.py
import os
import asyncio
from openai import AsyncOpenAI
from qdrant_client import AsyncQdrantClient

class RAGEngine:
    def __init__(self):
        self.client = AsyncOpenAI(
            api_key=os.getenv("GEMINI_API_KEY"),
            base_url="https://generativelanguage.googleapis.com/v1beta/openai/"  # ✅ no spaces
        )
        # ✅ Use same path as ingest.py
        self.qdrant = AsyncQdrantClient(path="./local_qdrant_physical")
        self.collection = "rag2"

    async def ask(self, question: str):
        # 1. Embed query
        emb_res = await self.client.embeddings.create(
            model="text-embedding-004",
            input=question
        )
        query_vector = emb_res.data[0].embedding

        # 2. ✅ Search (this works in qdrant-client >=1.8)
        hits = await self.qdrant.search(
            collection_name=self.collection,
            query_vector=query_vector,
            limit=2
        )

        # 3. Build context
        context = "\n\n---\n\n".join([
            f"{hit.payload.get('title', 'Section')}: {hit.payload.get('content', hit.payload.get('text', ''))}"
            for hit in hits
        ])

        if not context.strip():
            context = "No relevant content found in the textbook."

        # 4. Generate answer
        chat_res = await self.client.chat.completions.create(
            model="gemini-1.5-flash",
            messages=[
                {"role": "system", "content": "You are a robotics educator. Answer using ONLY the provided textbook content."},
                {"role": "user", "content": f"Context:\n{context}\n\nQuestion: {question}"}
            ],
            temperature=0.3
        )

        sources = [
            {"title": hit.payload.get("title", "Unknown"), "score": hit.score}
            for hit in hits
        ]

        return {
            "answer": chat_res.choices[0].message.content.strip(),
            "sources": sources
        }

    async def ask_selection(self, question: str, selection: str):
        # Use selected text only
        chat_res = await self.client.chat.completions.create(
            model="gemini-1.5-flash",
            messages=[
                {"role": "system", "content": "Explain the selected text clearly."},
                {"role": "user", "content": f"Selected text:\n{selection}\n\nQuestion: {question}"}
            ],
            temperature=0.2
        )
        return {"answer": chat_res.choices[0].message.content.strip()}