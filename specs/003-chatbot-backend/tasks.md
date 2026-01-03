---
description: "Task list for Chatbot Backend feature implementation"
---

# Tasks: Chatbot Backend

**Input**: Design documents from `/specs/003-chatbot-backend/`
**Prerequisites**: plan.md (required), spec.md (required), data-model.md

**Tests**: No explicit test tasks are included as they were not requested in the specification.

**Organization**: The primary functionality is grouped into a single user story (US1) representing the MVP.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1)
- Include exact file paths in descriptions

## Path Conventions

- Project Root: `chatbot-backend/`
- Source Code: `chatbot-backend/src/`
- Tests: `chatbot-backend/tests/`

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and dependency setup.

- [x] T001 Create the project directory structure: `chatbot-backend/src/api`, `src/core`, `src/services`, `src/models`, and `chatbot-backend/tests`.
- [x] T002 Create/update the `chatbot-backend/pyproject.toml` to include all required dependencies: `fastapi`, `uvicorn`, `python-dotenv`, `qdrant-client`, `langchain`, `google-genai`, `openai`, `fastembed`.
- [x] T003 Create a `.env.example` file in the `chatbot-backend` root for environment variable definitions (e.g., `QDRANT_URL`, `GOOGLE_API_KEY`, `OPENAI_API_KEY`).

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that must be complete before the main feature can be implemented.

- [x] T004 Implement the basic FastAPI application setup in `chatbot-backend/src/main.py`.
- [x] T005 [P] Create the data models (`ChatRequest`, `ChatResponse`, `Source`) as Pydantic schemas in `chatbot-backend/src/models/schema.py`.
- [x] T006 [P] Implement the Qdrant client connection and configuration in `chatbot-backend/src/core/database.py`.

---

## Phase 3: User Story 1 - RAG Chatbot Implementation (Priority: P1) 🎯 MVP

**Goal**: Implement the end-to-end Retrieval Augmented Generation pipeline.

**Independent Test**: After running the ingestion script, send a `POST` request to the `/api/chat` endpoint with a message and verify that a JSON response containing the chatbot's answer is returned.

### Implementation for User Story 1

- [x] T007 [US1] Implement the data ingestion logic in `chatbot-backend/src/ingest.py`. This script should read `book.txt`, split it into chunks, generate embeddings using `FastEmbed`, and store them in Qdrant.
- [x] T008 [US1] Create the core chat logic in `chatbot-backend/src/services/chat_service.py`. This service will orchestrate the RAG flow: embedding the user query, searching Qdrant for context, and calling the LLM with the combined prompt.
- [x] T009 [US1] Create the `/api/chat` endpoint in `chatbot-backend/src/main.py`. This endpoint will use the `ChatRequest` schema, call the `chat_service`, and return a `ChatResponse`.
- [x] T010 [US1] Add environment variable loading using `python-dotenv` in `chatbot-backend/src/main.py` and `chatbot-backend/src/ingest.py`.

---

## Phase 4: Polish & Cross-Cutting Concerns

**Purpose**: Final improvements for usability and documentation.

- [x] T011 Update `chatbot-backend/README.md` with clear instructions on how to set up the environment, run the ingestion script, and start the FastAPI server.
- [x] T012 [P] Add basic logging to the `chat_service` to record incoming queries and generated responses.
- [ ] T013 Validate the entire workflow by following the steps in `specs/003-chatbot-backend/quickstart.md`.

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: Can start immediately.
- **Foundational (Phase 2)**: Depends on Setup completion.
- **User Story 1 (Phase 3)**: Depends on Foundational phase completion.
- **Polish (Phase 4)**: Depends on User Story 1 completion.

### Within Each User Story

- **T008 (chat_service)** depends on **T007 (ingest)** being completed successfully first.
- **T009 (endpoint)** depends on **T008 (chat_service)** and **T005 (schemas)**.

### Parallel Opportunities

- **T005** and **T006** can be done in parallel during the Foundational phase.
- Once the Foundational phase is complete, the tasks within User Story 1 can be started, though they have some sequential dependencies as noted above.

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1.  Complete Phase 1: Setup.
2.  Complete Phase 2: Foundational.
3.  Complete Phase 3: User Story 1.
4.  **STOP and VALIDATE**: Run `ingest.py` and then test the `/api/chat` endpoint manually as described in the "Independent Test" section for US1.
5.  The MVP is considered delivered when the chat endpoint returns a valid response based on the ingested content.