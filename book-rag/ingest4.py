# backend/ingest.py
import os
from dotenv import load_dotenv
from openai import OpenAI
from qdrant_client import QdrantClient
from qdrant_client.models import VectorParams, Distance, PointStruct
import uuid

load_dotenv()

def main():
    # 🔑 Gemini client
    gemini = OpenAI(
        api_key=os.getenv("GEMINI_API_KEY"),
        base_url="https://generativelanguage.googleapis.com/v1beta/openai/"  # ✅ no spaces
    )

    # 📖 Load book.txt (must be in backend/)
    try:
        with open("book.txt", encoding="utf-8") as f:
            text = f.read().strip()
        if not text:
            raise ValueError("book.txt is empty!")
    except FileNotFoundError:
        print("❌ Create book.txt in backend/ with sample content:")
        print('echo "Docusaurus is a React-based static site generator. It helps build documentation websites." > book.txt')
        return

    # ✂️ Chunk
    chunks = [text[i:i+600] for i in range(0, len(text), 550)]
    chunks = [c.strip() for c in chunks if c.strip()]
    print(f"📦 {len(chunks)} chunks from book.txt")

    # 🧠 Embed
    print("🧠 Generating embeddings...")
    points = []
    for i, chunk in enumerate(chunks):
        print(f"  {i+1}/{len(chunks)}", end="\r")
        emb = gemini.embeddings.create(
            model="text-embedding-004",
            input=chunk
        ).data[0].embedding
        points.append(
            PointStruct(
                id=str(uuid.uuid4()),
                vector=emb,
                payload={"text": chunk, "source": "book.txt"}
            )
        )
    print()

    # 🗃️ Save to local_qdrant
    client = QdrantClient(path="./local_qdrant_v2")
    collection_name = "book_rag"  # ← consistent name

    # 🧹 Clean slate
    if client.collection_exists(collection_name):
        client.delete_collection(collection_name)
    
    client.create_collection(
        collection_name=collection_name,
        vectors_config=VectorParams(size=768, distance=Distance.COSINE)
    )
    
    client.upsert(collection_name=collection_name, points=points)
    print("✅ Success! Data saved to ./local_qdrant")
    print(f"   Collection: '{collection_name}'")
    print(f"   Points: {len(points)}")

if __name__ == "__main__":
    main()