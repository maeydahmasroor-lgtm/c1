# Quickstart Guide: Docusaurus Chatbot

This guide provides instructions to set up and run the Docusaurus chatbot project.

## Prerequisites

- Node.js and npm
- Python 3.11+
- `uv` (can be installed with `pip install uv`)
- Docker (for running Qdrant locally)

## 1. Backend Setup

1.  **Navigate to the backend directory:**
    ```bash
    cd backend
    ```

2.  **Set up the virtual environment:**
    ```bash
    uv venv
    ```

3.  **Create a `.env` file** and add your OpenAI API key:
    ```
    OPENAI_API_KEY="sk-..."
    ```

4.  **Create a `requirements.txt` file** with the following content:
    ```
    fastapi
    uvicorn[standard]
    openai
    qdrant-client
    sqlalchemy
    python-dotenv
    ```

5.  **Install dependencies:**
    ```bash
    uv pip install -r requirements.txt
    ```

6.  **Start Qdrant using Docker:**
    ```bash
    docker run -p 6333:6333 qdrant/qdrant
    ```

7.  **Run the data ingestion script** (this will be created in the implementation phase):
    ```bash
    # This is a placeholder for the actual command
    source .venv/bin/activate
    python src/data/ingest.py
    ```

8.  **Start the backend server:**
    ```bash
    uvicorn src.api.main:app --reload
    ```
    The backend will be running at `http://127.0.0.1:8000`.

## 2. Frontend Setup

1.  **Navigate to the Docusaurus project directory:**
    ```bash
    cd ai-robotics-mini-book
    ```

2.  **Install dependencies:**
    ```bash
    npm install
    ```

3.  **Swizzle the `Root` component:**
    ```bash
    npm run swizzle @docusaurus/theme-classic Root -- --eject
    ```
    This will create the `src/theme/Root.js` file.

4.  **Start the frontend development server:**
    ```bash
    npm start
    ```
    The Docusaurus site will be running at `http://localhost:3000`.

## 3. Running the Full Application

With both the backend and frontend servers running, you can open `http://localhost:3000` in your browser to see the book and interact with the chatbot.
