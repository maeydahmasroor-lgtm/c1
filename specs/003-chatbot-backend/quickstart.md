# Quickstart for Chatbot Backend

**Branch**: `003-chatbot-backend` | **Date**: 2026-01-02

This guide provides instructions for setting up and running the Chatbot Backend service.

## Prerequisites

- Python >=3.12
- `uv` package manager

## Setup

1.  **Clone the repository** (if you haven't already).

2.  **Navigate to the `chatbot-backend` directory**:
    ```bash
    cd chatbot-backend
    ```

3.  **Create a virtual environment and install dependencies**:
    ```bash
    uv venv
    uv pip install -r requirements.txt
    ```
    *(Note: You may need to generate a `requirements.txt` from `pyproject.toml` first using `uv pip freeze > requirements.txt`)*

4.  **Create a `.env` file**:
    Create a `.env` file in the `chatbot-backend` directory and add the necessary environment variables (e.g., API keys for OpenAI and Google Genai).
    ```
    GOOGLE_API_KEY="your-google-api-key"
    OPENAI_API_KEY="your-openai-api-key"
    QDRANT_URL="your-qdrant-url"
    QDRANT_API_KEY="your-qdrant-api-key"
    ```

## Running the Service

1.  **Activate the virtual environment**:
    ```bash
    source .venv/bin/activate
    ```
    (On Windows, use `.venv\Scripts\activate`)

2.  **Run the FastAPI application**:
    ```bash
    uvicorn src.api.main:app --reload
    ```
    *(Note: This assumes the main FastAPI app instance is in `src/api/main.py`)*

3.  **Access the API**:
    The API will be available at `http://127.0.0.1:8000`. You can access the auto-generated documentation at `http://127.0.0.1:8000/docs`.
