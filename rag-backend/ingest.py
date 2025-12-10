# ingest.py — Ingest your entire Docusaurus book into Qdrant using Gemini embeddings
# Run once (or whenever you add new chapters)

import os
import glob
import google.generativeai as genai
from qdrant_client import QdrantClient
from dotenv import load_dotenv

# Load secrets
load_dotenv()

# Configure Gemini
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

# Connect to Qdrant
qdrant = QdrantClient(
    url=os.getenv("QDRANT_URL"),
    api_key=os.getenv("QDRANT_API_KEY"),
)

COLLECTION_NAME = "book"
DIMENSION = 768  # Gemini embedding-001 dimension

# === 1. Recreate collection (clean start) ===
print("Creating/recreating collection...")
qdrant.recreate_collection(
    collection_name=COLLECTION_NAME,
    vectors_config={
        "size": DIMENSION,
        "distance": "Cosine",
    },
)

# === 2. Find all your book files ===
# Adjust this path if your Docusaurus project is named differently
DOCS_PATH = "../my-book/docs/**/*.mdx"        # supports .mdx and nested folders
# DOCS_PATH = "../my-book/docs/**/*.md"       # uncomment if you use .md

files = glob.glob(DOCS_PATH, recursive=True)
print(f"Found {len(files)} document files")

# === 3. Chunk + embed + upload ===
points = []
point_id = 0
batch_size = 100

for file_path in files:
    print(f"Processing: {file_path}")
    try:
        content = open(file_path, "r", encoding="utf-8").read()

        # Simple chunking (800 chars with 200 overlap → perfect for Gemini 1M context)
        chunks = []
        step = 800
        overlap = 200
        for i in range(0, len(content), step - overlap):
            chunk = content[i : i + step]
            if len(chunk.strip()) > 50:  # skip tiny chunks
                chunks.append(chunk)

        # Embed each chunk
        for chunk in chunks:
            embedding = genai.embed_content(
                model="models/embedding-001",
                content=chunk,
                task_type="retrieval_document",
            )["embedding"]

            points.append(
                {
                    "id": point_id,
                    "vector": embedding,
                    "payload": {
                        "text": chunk,
                        "source": os.path.relpath(file_path, "../my-book"),
                    },
                }
            )
            point_id += 1

            # Upload in batches
            if len(points) >= batch_size:
                qdrant.upsert(collection_name=COLLECTION_NAME, points=points)
                print(f"Uploaded {point_id} chunks...")
                points = []

    except Exception as e:
        print(f"Error with {file_path}: {e}")

# Final batch
if points:
    qdrant.upsert(collection_name=COLLECTION_NAME, points=points)

print(f"INGESTION COMPLETE! {point_id} chunks uploaded using Gemini")
print("Your book is now 100% ready for the RAG chatbot")