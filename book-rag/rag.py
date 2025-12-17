# backend/rag.py
import os
from dotenv import load_dotenv
from openai import AsyncOpenAI
from langchain_qdrant import QdrantVectorStore
from qdrant_client import QdrantClient
from langchain_openai import OpenAIEmbeddings

load_dotenv()

# Initialize once
embedding = OpenAIEmbeddings(
    api_key=os.getenv("GEMINI_API_KEY"),
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)

qdrant = QdrantVectorStore(
    client=QdrantClient(
        url=os.getenv("QDRANT_URL"),
        api_key=os.getenv("QDRANT_API_KEY")
    ),
    collection_name="book_rag",
    embedding=embedding
)

gemini_client = AsyncOpenAI(
    api_key=os.getenv("GEMINI_API_KEY"),
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)

async def query_rag(question: str, selected_text: str = None) -> str:
    # 🔍 Retrieve context (unless user selected text)
    if selected_text:
        context = selected_text
    else:
        docs = await qdrant.as_retriever(k=4).ainvoke(question)
        context = "\n\n---\n\n".join([f"[{d.metadata.get('chapter')}]: {d.page_content}" for d in docs])

    # 🧠 Generate with Gemini
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