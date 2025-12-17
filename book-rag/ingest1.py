# backend/ingest.py
import os
from dotenv import load_dotenv
from langchain_openai import OpenAIEmbeddings
from langchain_qdrant import QdrantVectorStore
from langchain_core.documents import Document
from qdrant_client import QdrantClient

load_dotenv()

def main():
    # Load book & chunk (simple)
    with open("book.txt", encoding="utf-8") as f:
        text = f.read()
    chunks = [text[i:i+600] for i in range(0, len(text), 550)]
    docs = [Document(page_content=c.strip()) for c in chunks if c.strip()]

    embeddings = OpenAIEmbeddings(
        api_key=os.getenv("GEMINI_API_KEY"),
        base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
    )

    client = QdrantClient(
        url=os.getenv("QDRANT_URL"),
        api_key=os.getenv("QDRANT_API_KEY"),
    )

    collection_name = "book_rag"
    
    # ✅ SAFE: Delete if exists, then create fresh
    if client.collection_exists(collection_name):
        print(f"🗑️  Deleting existing '{collection_name}'...")
        client.delete_collection(collection_name)

    print(f"🆕 Creating '{collection_name}' with {len(docs)} chunks...")
    #vector_store = QdrantVectorStore.from_documents(
    #    documents=docs,
    #    embedding=embeddings,
    #    collection_name="x12",
    #    url=os.getenv("QDRANT_URL"),        # ← use 'url', not 'client'
    #    api_key=os.getenv("QDRANT_API_KEY"),  # ← use 'api_key'
    #    force_recreate=True,
    #)
    client.recreate_collection(
    collection_name="rag",
    vectors_config=VectorParams(size=1536, distance=Distance.COSINE),
)

# 3. Upsert points
    points = [
        PointStruct(
        id=idx,
        vector=embeddings.embed_query(doc.page_content),
        payload={"test": doc.page_content}
        ) for idx, doc in enumerate(docs)
    ]

    client.upsert(collection_name="rag", points=points)
    print("✅ Success!")

if __name__ == "__main__":
    main()