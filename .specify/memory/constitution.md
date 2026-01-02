<!--
    Sync Impact Report

    - Version change: 2.0.0 -> 3.0.0
    - Modified principles:
        - 1. Retrieval-Augmented Generation (RAG) Chatbot -> 1. FastAPI for REST endpoints
        - 2. Technology Stack -> 2. Qdrant for vector DB
        - 3. Core Functionality -> 3. Gemini for embedding
    - Added sections:
        - 4. Gemini for answer generation
        - 5. Token counting and context truncation
        - 6. Environment variables with python-dotenv
        - 7. Clean, modular, and type-annotated code
        - 8. Prompt and context optimization
    - Removed sections: None
    - Templates requiring updates:
        - ✅ .specify/templates/plan-template.md (No changes needed)
        - ✅ .specify/templates/spec-template.md (No changes needed)
        - ✅ .specify/templates/tasks-template.md (No changes needed)
    - Follow-up TODOs: None
-->
# Integrated RAG Chatbot Development: A Mini-Book Constitution

## Core Principles

### 1. FastAPI for REST endpoints
Use FastAPI for REST endpoints (/ingest, /chat).

### 2. Qdrant for vector DB
Use Qdrant (local or cloud) as vector DB with collection "book_collection".

### 3. Gemini for embedding
Embed with Gemini embedding-001 via LangChain.

### 4. Gemini for answer generation
Generate answers with gemini-1.5-flash.

### 5. Token counting and context truncation
Always count tokens using genai.count_tokens before generation; truncate context if total > 800_000 tokens.

### 6. Environment variables with python-dotenv
Load env vars with python-dotenv.

### 7. Clean, modular, and type-annotated code
Write clean, modular, type-annotated code with error handling.

### 8. Prompt and context optimization
Optimize prompts and context for minimal token usage.


## Governance
This constitution represents the creative vision for the "Integrated RAG Chatbot Development" mini-book. All content must align with these three principles. Amendments to the narrative require a revision of this document to maintain conceptual integrity.

**Version**: 3.0.0 | **Ratified**: 2025-12-10 | **Last Amended**: 2026-01-02
