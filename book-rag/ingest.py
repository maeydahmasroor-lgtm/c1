# backend/ingest.py
import os
import re
from dotenv import load_dotenv
from langchain_openai import OpenAIEmbeddings
from langchain_qdrant import QdrantVectorStore
from langchain_core.documents import Document
from qdrant_client import QdrantClient

load_dotenv()

def simple_recursive_split(text: str, chunk_size: int = 600, chunk_overlap: int = 50) -> list[str]:
    if not text.strip():
        return []
    chunks = [p.strip() for p in text.split("\n\n") if p.strip()]
    refined = []
    for chunk in chunks:
        if len(chunk) > chunk_size:
            subchunks = [s.strip() for s in chunk.split("\n") if s.strip()]
            refined.extend(subchunks)
        else:
            refined.append(chunk)
    final = []
    for chunk in refined:
        if len(chunk) <= chunk_size:
            final.append(chunk)
        else:
            sentences = re.split(r'(?<=[.!?])\s+', chunk)
            current = ""
            for sent in sentences:
                if len(current) + len(sent) + 1 <= chunk_size:
                    current = current + " " + sent if current else sent
                else:
                    if current:
                        final.append(current.strip())
                    current = sent
            if current:
                final.append(current.strip())
    result = []
    i = 0
    while i < len(final):
        chunk = final[i]
        while i + 1 < len(final) and len(chunk) + len(final[i+1]) + 1 <= chunk_size:
            chunk += " " + final[i+1]
            i += 1
        result.append(chunk)
        i += 1
    overlapped = []
    for i, chunk in enumerate(result):
        if i == 0:
            overlapped.append(chunk)
        else:
            prev = overlapped[-1]
            overlap_start = max(0, len(prev) - chunk_overlap)
            combined = prev[overlap_start:] + " " + chunk
            overlapped.append(combined[:chunk_size])
    return overlapped

def main():
    # 🔑 Validate env
    for key in ["GEMINI_API_KEY", "QDRANT_URL", "QDRANT_API_KEY"]:
        if not os.getenv(key):
            raise RuntimeError(f"❌ Missing {key} in .env")

    # 📖 Load book.txt (now in SAME folder as ingest.py for simplicity)
    with open("book.txt", encoding="utf-8") as f:
        text = f.read()

    # ✂️ Split
    chunks = simple_recursive_split(text, chunk_size=600, chunk_overlap=50)
    docs = [
        Document(page_content=chunk.strip(), metadata={"source": "book.txt"})
        for chunk in chunks if chunk.strip()
    ]
    print(f"📦 Created {len(docs)} chunks")

    # 🧠 Embeddings (✅ fixed base_url: NO TRAILING SPACE!)
    embeddings = OpenAIEmbeddings(
        api_key=os.getenv("GEMINI_API_KEY"),
        base_url="https://generativelanguage.googleapis.com/v1beta/openai/"  # ← removed trailing spaces!
    )

    # 🗃️ ✅ CORRECT WAY: Pass url/api_key directly to QdrantVectorStore
    vector_store = QdrantVectorStore.from_documents(
        documents=docs,
        embedding=embeddings,
        collection_name="x",
        url=os.getenv("QDRANT_URL"),        # ← use 'url', not 'client'
        api_key=os.getenv("QDRANT_API_KEY"),  # ← use 'api_key'
        force_recreate=True,
    )

    print("✅ Ingest complete!")

if __name__ == "__main__":
    main()