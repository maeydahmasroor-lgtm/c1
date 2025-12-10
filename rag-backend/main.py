# main.py — Docusaurus RAG Backend powered by Google Gemini 1.5 Flash
# Fully Constitutional | Zero OpenAI | Uses only free Gemini tier

import os
from uuid import uuid4
from fastapi import FastAPI, Body
from fastapi.middleware.cors import CORSMiddleware
from qdrant_client import QdrantClient
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

app = FastAPI(title="Docusaurus Book RAG – Gemini Edition", version="1.0")

# === SECURITY ===
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # ← change to your domain in prod
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# === Gemini setup ===
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

# === Qdrant ===
qdrant = QdrantClient(
    url=os.getenv("QDRANT_URL"),
    api_key=os.getenv("QDRANT_API_KEY"),
)
COLLECTION_NAME = "book"


@app.on_event("startup")
async def startup():
    if not qdrant.has_collection(COLLECTION_NAME):
        qdrant.create_collection(
            collection_name=COLLECTION_NAME,
            vectors_config={"size": 768, "distance": "Cosine"},  # Gemini embedding-001 = 768 dim
        )


@app.post("/chat")
async def chat(
    query: str = Body(..., embed=True),
    selected_text: str = Body(None, embed=True),
    session_id: str = Body(None, embed=True),
):
    if not session_id:
        session_id = str(uuid4())

    # 1. Embed query with Gemini
    query_embedding = genai.embed_content(
        model="models/embedding-001",
        content=query,
        task_type="retrieval_query",
    )#["embedding"]

    # 2. Search Qdrant
    hits = qdrant.search(
        collection_name=COLLECTION_NAME,
        query_vector=query_embedding,
        limit=6,  # Gemini loves a bit more context
    )

    context = "\n\n".join([hit.payload["text"] for hit in hits])

    # 3. Selected text is supreme (Constitution rule #2)
    if selected_text and selected_text.strip():
        context = f"USER SELECTED THIS EXACT TEXT:\n{selected_text.strip()}\n\nRELEVANT BOOK PASSAGES:\n{context}"

    # 4. Generate with Gemini 1.5 Flash (free, fast, 1M context)
    model = genai.GenerativeModel(
        model_name="gemini-1.5-flash",
        generation_config={
            "temperature": 0.0,
            "max_output_tokens": 800,
        },
        safety_settings=None,  # you control safety via prompt
    )

    prompt = f"""You are an assistant for a published book. 
Answer the question using ONLY the context below.
If the answer is not there, reply exactly: "I don't know."

Context:
{context}

Question: {query}"""

    response = model.generate_content(prompt)

    answer = response.text if response.text else "I don't know."

    return {
        "response": answer.strip(),
        "session_id": session_id,
    }
