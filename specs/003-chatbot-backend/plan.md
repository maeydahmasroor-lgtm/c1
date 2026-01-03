# Implementation Plan: Chatbot Backend

**Branch**: `003-chatbot-backend` | **Date**: 2026-01-02 | **Spec**: [spec.md](./spec.md)
**Input**: Feature specification from `C:/Users/Adminstrator/Documents/rag/c2/specs/003-chatbot-backend/spec.md`

**Note**: This template is filled in by the `/sp.plan` command. See `.specify/templates/commands/plan.md` for the execution workflow.

## Summary

This feature implements the backend service for a chatbot. The service will expose a RESTful API for handling chat messages, and it will integrate with a vector database (Qdrant) and large language models (OpenAI, Google Genai) via LangChain to provide intelligent responses. The technical approach is based on a Python backend using FastAPI.

## Technical Context

**Language/Version**: Python >=3.12
**Primary Dependencies**: FastAPI, LangChain, Qdrant-client, google-genai, openai
**Storage**: Qdrant
**Testing**: pytest (NEEDS CLARIFICATION)
**Target Platform**: Linux server
**Project Type**: Web application
**Performance Goals**: < 500ms p95 response time (NEEDS CLARIFICATION)
**Constraints**: Must support 10 concurrent users (NEEDS CLARIFICATION)
**Scale/Scope**: Initial prototype for a mini-book (NEEDS CLARIFICATION)

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

*   **[MATCH]** Principle 1: FastAPI for REST endpoints
*   **[MATCH]** Principle 2: Qdrant for vector DB
*   **[VIOLATION]** Principle 3: Gemini for embedding. `spec.md` implies `FastEmbed`, but constitution requires `Gemini embedding-001`.
*   **[PARTIAL VIOLATION]** Principle 4: Gemini for answer generation. `spec.md` includes `OpenAI`, which is not in the constitution's `gemini-1.5-flash`.
*   **[NEEDS CLARIFICATION]** Principle 5: Token counting and context truncation.
*   **[MATCH]** Principle 6: Environment variables with python-dotenv.
*   **[PASS]** Principle 7: Clean, modular, and type-annotated code.
*   **[PASS]** Principle 8: Prompt and context optimization.

## Project Structure

### Documentation (this feature)

```text
specs/003-chatbot-backend/
├── plan.md              # This file (/sp.plan command output)
├── research.md          # Phase 0 output (/sp.plan command)
├── data-model.md        # Phase 1 output (/sp.plan command)
├── quickstart.md        # Phase 1 output (/sp.plan command)
├── contracts/           # Phase 1 output (/sp.plan command)
└── tasks.md             # Phase 2 output (/sp.tasks command - NOT created by /sp.plan)
```

### Source Code (repository root)
```text
# Option 1: Single project (DEFAULT)
chatbot-backend/
├── src/
│   ├── api/
│   ├── core/
│   ├── services/
│   ├── models/
│   ├── main.py
│   ├── ingest.py
│   └── schema.py
└── tests/
    ├── integration/
    └── unit/
```

**Structure Decision**: The project will follow the "Single project" structure, building upon the existing `chatbot-backend` directory. New source code will be organized within a `src` directory, and tests will be placed in a `tests` directory, as is common practice for Python applications.

## Implementation Details

### Qdrant Client Setup
- Initialize the Qdrant client to connect to the vector database.
- Configuration will be handled via environment variables.
- Create a new collection if it doesn't exist, with the appropriate vector parameters (size, distance metric).

### Ingestion Flow
- `ingest.py` will be the main script for data ingestion.
- It will read the source `book.txt` file.
- The text will be split into chunks.
- Embeddings will be generated for each chunk using the configured embedding model.
- The chunks and their corresponding embeddings will be stored in the Qdrant collection.

### Chat Flow with Token Management
- The main chat logic will be in `src/services/chat_service.py`.
- It will receive a user query.
- It will generate an embedding for the query.
- It will search Qdrant for similar vectors to retrieve relevant context.
- It will construct a prompt for the LLM, including the user query and the retrieved context.
- It will call the LLM to get a response.
- Token management will be implemented to ensure the context window of the LLM is not exceeded. This includes truncating the context if necessary.

### FastAPI App and Routes
- `main.py` will contain the FastAPI application.
- It will define the API routes (e.g., `/chat`).
- The `/chat` route will handle POST requests with the user's message.
- It will use the chat service to get a response and return it to the user.
- API request and response models will be defined in `src/schema.py`.

## Complexity Tracking

> **Fill ONLY if Constitution Check has violations that must be justified**

| Violation | Why Needed | Simpler Alternative Rejected Because |
|-----------|------------|-------------------------------------|
| Using `FastEmbed` instead of `Gemini embedding-001` | The initial `pyproject.toml` for the `chatbot-backend` project specified `fastembed`. This might be a deliberate choice for performance, offline capability, or cost. | Sticking to the constitution's `Gemini embedding-001` would require removing an existing dependency and might conflict with the original project's goals. This needs clarification. |
| Including `OpenAI` as an LLM provider | The project might be designed to compare or switch between different LLM providers, offering more flexibility. | Restricting to only `gemini-1.5-flash` would remove flexibility that seems to be intended by the project's dependencies. This needs clarification. |