# Tasks: Docusaurus Chatbot

**Feature**: `002-docusaurus-chatbot`

This document outlines the implementation tasks for the Docusaurus Chatbot feature, ordered by dependency. This plan has been updated to reflect a root-level backend structure.

## Implementation Strategy

The implementation will follow an MVP-first approach. We will start with setting up the project structure and foundational elements. Then, we will implement each user story as an independent, testable increment, starting with the highest priority stories (US1 and US2).

## Phase 1: Project Setup

*Goal: Initialize the project structure for both the backend and frontend.*

- [X] T001 Create the Python project structure: `src/api`, `src/core`, `src/models`, `src/services`, `src/data`, `tests` at the repository root.
- [X] T002 Initialize a Python virtual environment by running `uv venv venv`.
- [X] T003 Create a `pyproject.toml` file at the root to manage Python dependencies.
- [X] T004 Activate the virtual environment (`.\venv\Scripts\activate`) and add dependencies by running `uv add fastapi uvicorn openai qdrant-client sqlalchemy python-dotenv beautifulsoup4 lxml`.
- [X] T005 Create a `.env` file at the root and add `OPENAI_API_KEY=""`.
- [C] T006 Create a `docker-compose.yml` file at the root to run a Qdrant instance.
- [X] T007 [P] In the `ai-robotics-mini-book` directory, run `npm install` to ensure all Docusaurus dependencies are present.
- [X] T008 [P] In the `ai-robotics-mini-book` directory, swizzle the Docusaurus Root component by running `npm run swizzle @docusaurus/theme-classic Root -- --eject` to create `src/theme/Root.js`.

## Phase 2: Foundational Tasks

*Goal: Implement blocking prerequisites for all user stories, including data ingestion and basic UI shells.*

- [X] T009 Create the data ingestion script in `src/data/ingest.py` to read markdown files from `ai-robotics-mini-book/docs`, chunk them, and generate embeddings.
- [ ] T010 [P] Implement the Qdrant client and a service in `src/services/qdrant_service.py` to store the embedded chunks in the `docusaurus_book` collection.
- [ ] T011 Implement the core FastAPI application setup in `src/main.py`, including basic configuration.
- [ ] T012 Implement the database connection and SQLAlchemy setup in `src/core/database.py`.
- [ ] T013 [P] Create the basic React component structure for the chatbot in `ai-robotics-mini-book/src/components/Chatbot/index.tsx`, including a floating button and an empty chat window.
- [ ] T014 [P] Create the CSS file `ai-robotics-mini-book/src/components/Chatbot/styles.module.css` for the chatbot component.

## Phase 3: User Story 1 - Get a Relevant Answer (P1)

*Goal: Users can ask a question and receive a relevant answer from the book's content.*
*Independent Test: Ask a question clearly answered in the book and verify a relevant answer is returned.*

- [ ] T015 [US1] Implement SQLAlchemy models for `Conversation` and `Message` in `src/models/chat.py`.
- [ ] T016 [US1] Create database migration/creation logic based on the SQLAlchemy models.
- [ ] T017 [US1] In `src/services/qdrant_service.py`, implement the function to retrieve relevant context for a user query.
- [ ] T018 [US1] Create a new service `src/services/openai_service.py` to generate an answer from the retrieved context using the OpenAI API.
- [ ] T019 [US1] Implement the `POST /api/chat` endpoint in `src/api/chat.py` to orchestrate the services.
- [ ] T020 [P] [US1] In `ai-robotics-mini-book/src/theme/Root.js`, wrap the application with a context provider for chatbot state.
- [ ] T021 [US1] In `ai-robotics-mini-book/src/components/Chatbot/index.tsx`, implement state management for the conversation.
- [ ] T022 [US1] In `ai-robotics-mini-book/src/components/Chatbot/index.tsx`, implement the API call to `POST /api/chat` and display the streaming response.

## Phase 4: User Story 2 - Handle Out-of-Scope Questions (P1)

*Goal: The system politely declines to answer questions not covered in the book.*
*Independent Test: Ask a generic question and verify the system provides the specified decline message.*

- [ ] T023 [US2] In `src/services/openai_service.py`, update the prompt to instruct the model to decline questions if the context is not relevant.
- [ ] T024 [US2] In `src/api/chat.py`, add logic to detect low-relevance context and trigger the "I can only answer..." response.

## Phase 5: User Story 3 - Graceful Error Handling (P2)

*Goal: The user sees a clear error message if the service has a problem.*
*Independent Test: Simulate an API error and check that a user-friendly error message is displayed.*

- [ ] T025 [US3] In `src/api/chat.py`, add exception handling for external service calls.
- [ ] T026 [US3] In `ai-robotics-mini-book/src/components/Chatbot/index.tsx`, update the API client to handle non-200 responses and display an error message.

## Phase 6: Polish & Cross-Cutting Concerns

*Goal: Finalize styling, documentation, and configuration.*

- [ ] T027 [P] Refine the chatbot UI/UX in `ai-robotics-mini-book/src/components/Chatbot/styles.module.css`.
- [ ] T028 Add a `README.md` to the root directory with setup and run instructions for the backend.
- [ ] T029 Review and finalize environment variable handling in `src/core/config.py`.

## Dependencies

- **User Story 1** is a prerequisite for all other user stories.
- **User Story 2** and **User Story 3** can be implemented in parallel after User Story 1 is complete.

## Parallel Execution

- **Phase 1**: `T007` and `T008` (frontend setup) can be run in parallel with the backend setup tasks.
- **Phase 2**: `T010`, `T013`, and `T014` are marked with `[P]` and can be worked on in parallel.
- **Phase 3**: `T020` (frontend Root component) can be worked on in parallel with the backend service implementations.