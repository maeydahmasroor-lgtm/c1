# backend/ingest.py
import os
from dotenv import load_dotenv
from openai import OpenAI
from qdrant_client import QdrantClient
from qdrant_client.models import VectorParams, Distance, PointStruct
import uuid

load_dotenv()

def main():
    # 🔑 Gemini client (✅ no trailing spaces!)
    gemini = OpenAI(
        api_key=os.getenv("GEMINI_API_KEY"),
        base_url="https://generativelanguage.googleapis.com/v1beta/openai/"  # ✅ clean
    )

    # 📖 Load your book.txt (must be in backend/ folder)
    try:
        with open("book.txt", "r", encoding="utf-8") as f:
            book_text = f.read().strip()
        print(f"✅ Loaded book.txt ({len(book_text):,} characters)")
    except FileNotFoundError:
        raise FileNotFoundError("❌ book.txt not found in backend/ folder")

    # ✂️ Simple chunking (no headers needed)
    CHUNK_SIZE = 600
    chunks = [
        book_text[i:i + CHUNK_SIZE]
        for i in range(0, len(book_text), CHUNK_SIZE - 100)  # 100-char overlap
    ]
    chunks = [c.strip() for c in chunks if c.strip()]
    print(f"📦 Created {len(chunks)} chunks")

    # 🧠 Embed & store
    points = []
    for i, chunk in enumerate(chunks):
        print(f"  {i+1}/{len(chunks)}", end="\r")
        emb = gemini.embeddings.create(
            model="text-embedding-004",
            input=chunk
        ).data[0].embedding
        
        points.append(PointStruct(
            id=str(uuid.uuid4()),
            vector=emb,
            payload={"text": chunk}
        ))

    # 🗃️ Save to Qdrant
    client = QdrantClient(path="./local_qdrant_physical")
    collection = "physical_ai_book"
    
    if client.collection_exists(collection):
        client.delete_collection(collection)
    
    client.create_collection(
        collection_name=collection,
        vectors_config=VectorParams(size=768, distance=Distance.COSINE)
    )
    
    client.upsert(collection_name=collection, points=points)
    print("\n✅ Success! Book ingested into Qdrant.")

if __name__ == "__main__":
    main()