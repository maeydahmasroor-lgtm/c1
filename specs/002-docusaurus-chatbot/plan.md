# Implementation Plan: Docusaurus Chatbot

**Branch**: `002-docusaurus-chatbot` | **Date**: 2025-12-12 | **Spec**: [spec.md](./spec.md)
**Input**: Feature specification from `specs/002-docusaurus-chatbot/spec.md`

**Note**: This template is filled in by the `/sp.plan` command. See `.specify/templates/commands/plan.md` for the execution workflow.

## Summary

This plan outlines the implementation of a RAG (Retrieval-Augmented Generation) chatbot embedded within a Docusaurus book. The chatbot will answer user questions based on the book's content. The backend will be a FastAPI application, served by Uvicorn, using a `uv` managed virtual environment. It will leverage OpenAI for generating answers, Qdrant as a vector database for retrieval, and SQLite for storing conversation history. The frontend will involve creating a new `chatbot.ts` React component and integrating it into the Docusaurus application by swizzling the root component.

## Technical Context

**Language/Version**: Python 3.11+, TypeScript
**Primary Dependencies**:
  - **Backend**: `fastapi`, `uvicorn`, `openai`, `qdrant-client`, `sqlalchemy`
  - **Frontend**: `react`, `docusaurus`
**Storage**: Qdrant (vector store), SQLite (conversation history)
**Testing**: `pytest`
**Target Platform**: Web (Docusaurus)
**Project Type**: Web application (frontend + backend)
**Performance Goals**: p95 response time < 3 seconds [NEEDS CLARIFICATION]
**Constraints**: Must decline out-of-scope questions and handle API errors gracefully. The book's content source format needs to be defined.
**Scale/Scope**: A chatbot for a single Docusaurus-based book.

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

- **Principle 1: RAG Chatbot**: PASS. The plan is to build a RAG chatbot.
- **Principle 2: Technology Stack**: VIOLATION. The constitution specifies `Neon Serverless Postgres`, but the user request specifies `sqlite`. This deviation is justified below. All other technologies (`OpenAI`, `FastAPI`, `Qdrant`) are aligned.
- **Principle 3: Core Functionality**: PASS. The plan is to answer questions based on book content.

## Project Structure

### Documentation (this feature)

```text
specs/002-docusaurus-chatbot/
├── plan.md              # This file (/sp.plan command output)
├── research.md          # Phase 0 output (/sp.plan command)
├── data-model.md        # Phase 1 output (/sp.plan command)
├── quickstart.md        # Phase 1 output (/sp.plan command)
├── contracts/           # Phase 1 output (/sp.plan command)
└── tasks.md             # Phase 2 output (/sp.tasks command - NOT created by /sp.plan)
```

### Source Code (repository root)
```text
book-rag/
├── .venv/                 # Python virtual environment
├── book.txt               # Your book/content to ingest
├── ingest.py              # Script to ingest book into vector DB
├── main.py                # FastAPI app (RAG chat endpoint)

ai-robotics-mini-book/  # Existing Docusaurus project
├── src/
│   ├── components/
│   │   └── Chatbot/
│   │       ├── index.ts # Main chatbot component logic
│   │       └── styles.css
│   └── theme/
│       └── Root.js      # Swizzled Root component to wrap the app
└── ... (rest of docusaurus structure)
```

**Structure Decision**: The project is split into a `backend` directory for the FastAPI application and the existing `ai-robotics-mini-book` directory for the Docusaurus frontend. This aligns with the "Web application" structure and provides a clean separation of concerns.

## Complexity Tracking

> **Fill ONLY if Constitution Check has violations that must be justified**

| Violation | Why Needed | Simpler Alternative Rejected Because |
|-----------|------------|-------------------------------------|
| Using `sqlite` instead of `Neon Serverless Postgres` | The user explicitly requested `sqlite` in the prompt. For a simple use case of storing chat history, SQLite is lightweight and sufficient, avoiding the need for external service provisioning. | `Neon Serverless Postgres` was rejected to adhere to the user's direct request and to simplify the local development setup. |
