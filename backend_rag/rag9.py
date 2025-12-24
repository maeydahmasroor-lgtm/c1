from qdrant_client import QdrantClient, models
from fastembed import TextEmbedding
import google.generativeai as genai
import os

# -----------------------------
# Qdrant Cloud
# -----------------------------
client = QdrantClient(
    url=os.getenv("QDRANT_URL"),
    api_key=os.getenv("QDRANT_API_KEY")
)

collection_name = "book_collection"

# -----------------------------
# Embeddings
# -----------------------------
embedding_model = TextEmbedding(model_name="BAAI/bge-small-en-v1.5")

# -----------------------------
# Load & index book (run once)
# -----------------------------
def index_book():
    with open("book.txt", "r", encoding="utf-8") as f:
        text = f.read()

    chunks = [
        text[i:i+1000]
        for i in range(0, len(text), 1000)
    ]

    embeddings = list(embedding_model.embed(chunks))
    dim = len(embeddings[0])

    if not client.collection_exists(collection_name):
        client.create_collection(
            collection_name=collection_name,
            vectors_config=models.VectorParams(
                size=dim,
                distance=models.Distance.COSINE
            )
        )

        points = [
            models.PointStruct(
                id=i,
                vector=embeddings[i],
                payload={"text": chunks[i]}
            )
            for i in range(len(chunks))
        ]

        client.upload_points(collection_name, points)

index_book()

# -----------------------------
# RAG Query
# -----------------------------
def query_rag(question: str, selected_text: str | None = None) -> str:

    query_vector = list(embedding_model.embed(question))[0]

    hits = client.query_points(
        collection_name=collection_name,
        query=query_vector,
        limit=5
    )

    context = "\n\n".join(p.payload["text"] for p in hits.points)

    if selected_text:
        context = selected_text + "\n\n" + context

    genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
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
