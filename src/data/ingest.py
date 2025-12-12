import os
import openai
from dotenv import load_dotenv
from langchain.text_splitter import RecursiveCharacterTextSplitter

# Load environment variables from .env file
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

DOCS_PATH = os.path.join("ai-robotics-mini-book", "docs")

def load_documents(docs_path):
    documents = []
    for root, _, files in os.walk(docs_path):
        for file in files:
            if file.endswith(".md") or file.endswith(".mdx"):
                filepath = os.path.join(root, file)
                with open(filepath, "r", encoding="utf-8") as f:
                    documents.append({"content": f.read(), "source": filepath})
    return documents

def chunk_documents(documents):
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200,
        length_function=len,
        add_start_index=True,
    )
    chunks = []
    for doc in documents:
        content = doc["content"]
        metadata = {"source": doc["source"]}
        doc_chunks = text_splitter.create_documents([content], [metadata])
        chunks.extend(doc_chunks)
    return chunks

def generate_embeddings(chunks):
    # This will be implemented in T010, which involves Qdrant
    # For T009, we just need to ensure the chunks are ready for embedding
    # and potentially mock the embedding generation or return dummy data
    # to test the ingestion pipeline up to this point.
    print(f"Generating embeddings for {len(chunks)} chunks...")
    # In a real scenario, you'd call OpenAI's embedding API here:
    # response = openai.Embedding.create(
    #     input=[chunk.page_content for chunk in chunks],
    #     model="text-embedding-ada-002"
    # )
    # embeddings = [item['embedding'] for item in response['data']]
    # return embeddings
    return [{"chunk_id": i, "embedding": [0.1] * 1536, "text": chunk.page_content, "metadata": chunk.metadata} for i, chunk in enumerate(chunks)]

def ingest_data():
    print("Starting data ingestion...")
    documents = load_documents(DOCS_PATH)
    print(f"Loaded {len(documents)} documents.")
    
    chunks = chunk_documents(documents)
    print(f"Created {len(chunks)} chunks.")
    
    # This part will be fully integrated with Qdrant in T010
    embeddings_data = generate_embeddings(chunks)
    print("Finished generating embeddings (mock data).")

    print("Data ingestion complete.")
    return embeddings_data

if __name__ == "__main__":
    ingest_data()
