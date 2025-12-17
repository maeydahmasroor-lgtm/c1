# backend/ingest.py
import os
import uuid
from dotenv import load_dotenv
from openai import OpenAI
from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams, PointStruct

load_dotenv()

def main():
    # 🔑 Validate
    for key in ["GEMINI_API_KEY", "QDRANT_URL", "QDRANT_API_KEY1"]:
        if not os.getenv(key):
            raise RuntimeError(f"❌ Missing {key} in .env")

    # 📖 Load book
    with open("book.txt", encoding="utf-8") as f:
        text = f.read()

    # ✂️ Simple chunking
    chunks = [text[i:i+600] for i in range(0, len(text), 550)]
    chunks = [c.strip() for c in chunks if c.strip()]
    print(f"📦 {len(chunks)} chunks ready")

    # 🧠 Embed with Gemini (via OpenAI API)
    gemini = OpenAI(
        api_key=os.getenv("GEMINI_API_KEY"),
        base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
    )

    print("🧠 Generating embeddings...")
    embeddings = []
    for i, chunk in enumerate(chunks):
        print(f"  {i+1}/{len(chunks)}", end="\r")
        emb = gemini.embeddings.create(
            model="text-embedding-004",  # ✅ Gemini's embedding model
            input=chunk
        ).data[0].embedding
        embeddings.append(emb)
    print(f"\n✅ {len(embeddings)} embeddings generated")

    # 🗃️ Connect to Qdrant
    client = QdrantClient(
        url=os.getenv("QDRANT_URL"),
        api_key=os.getenv("QDRANT_API_KEY1"),
        timeout=30
    )

    collection_name = "MAEYDA1"

    # 🧹 Delete if exists
    if client.collection_exists(collection_name):
        print(f"🗑️  Deleting existing '{collection_name}'")
        client.delete_collection(collection_name)

    # ➕ Create collection
    client.create_collection(
        collection_name=collection_name,
        vectors_config=VectorParams(size=768, distance=Distance.COSINE)  # text-embedding-004 = 768-dim
    )
    print(f"🆕 Collection '{collection_name}' created")

    # 📤 Upload points
    points = [
        PointStruct(
            id=str(uuid.uuid4()),
            vector=emb,
            payload={"text": chunk, "source": "book.txt"}
        )
        for chunk, emb in zip(chunks, embeddings)
    ]

    print(f"📤 Uploading {len(points)} points...")
    client.upsert(collection_name=collection_name, points=points)
    print("✅ Success! Check Qdrant Cloud dashboard.")

if __name__ == "__main__":
    main()