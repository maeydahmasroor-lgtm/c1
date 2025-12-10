---

description: "Task list for AI Robotics & Humanoids: Chatbot Feature"
---

# Tasks: AI Robotics & Humanoids: Chatbot Feature

**Input**: Design documents from `/specs/001-constitution-principles/`
**Prerequisites**: plan.md (required), spec.md (required for user stories)

**Tests**: Tests are not explicitly requested in the feature specification, so task generation focuses on implementation and manual verification.

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

## Path Conventions

- **RAG Backend**: `rag-backend/`
- **Docusaurus Frontend**: `ai-robotics-mini-book/`

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and basic structure for the RAG backend.

- [X] T001 Create `rag-backend` directory at project root.
- [X] T002 Initialize Python virtual environment in `rag-backend/`.
- [X] T003 Create `requirements.txt` in `rag-backend/` with:
    ```
    fastapi
    uvicorn
    qdrant-client
    google-generativeai
    python-dotenv
    fastapi-cors
    ```
- [X] T004 Install Python dependencies from `rag-backend/requirements.txt` into the virtual environment.
- [X] T005 Create `.env` file in `rag-backend/` with placeholder values for `GEMINI_API_KEY`, `QDRANT_URL`, `QDRANT_API_KEY`.

---

## Phase 2: Foundational (Backend Core Implementation)

**Purpose**: Implement the core RAG backend services.

- [X] T006 Create `main.py` in `rag-backend/` with the provided FastAPI code.
- [X] T007 Create `ingest.py` in `rag-backend/` with the provided ingestion script.

---

## Phase 3: User Story 1 - Core RAG Backend Functionality (Adherence to Content Origin & Prioritization of Highlighted Text)

**Goal**: Establish a functional RAG backend that can ingest book content and respond to queries based *only* on that content, prioritizing selected text.

**Independent Test**: Verify that the FastAPI application runs, serves API documentation, and can successfully respond to queries using ingested book data, adhering to content constraints.

### Implementation for User Story 1

- [ ] T008 Run FastAPI backend locally using `uvicorn rag-backend/main.py`.
- [ ] T009 Access API documentation at `http://127.0.0.1:8000/docs` for FastAPI backend to confirm setup.
- [ ] T010 Update `DOCS_PATH` variable in `rag-backend/ingest.py` to point to `../ai-robotics-mini-book/docs/**/*.mdx`.
- [ ] T011 Execute `ingest.py` locally to populate Qdrant with initial data from the book (`python rag-backend/ingest.py`).
- [ ] T012 Test the `/chat` endpoint manually (e.g., using Swagger UI or Postman) with sample queries and verify responses are from the book content.
- [ ] T013 Test the `/chat` endpoint with a `selected_text` parameter and verify its prioritization.

**Checkpoint**: At this point, User Story 1 (core RAG backend) should be fully functional and testable independently.

---

## Phase 4: User Story 2 - AI Chat Widget Integration & UI (No third-party, single bubble, mobile/dark mode, offline)

**Goal**: Integrate a Docusaurus-compliant AI chat widget into the frontend, ensuring it meets all constitutional UI/UX requirements.

**Independent Test**: Verify the chat widget appears, functions, adheres to styling, works on mobile, adapts to dark mode, and shows "no connection" offline.

### Implementation for User Story 2

- [ ] T014 Create `src/components/AIChat/` directory in `ai-robotics-mini-book/`.
- [ ] T015 Create `index.js` in `ai-robotics-mini-book/src/components/AIChat/` with the provided React widget code.
- [ ] T016 Update `API_URL` constant in `ai-robotics-mini-book/src/components/AIChat/index.js` to point to the locally running backend URL (e.g., `http://127.0.0.1:8000`).
- [ ] T017 Create or edit `src/theme/Root.js` in `ai-robotics-mini-book/` to inject the `<AIChat />` component.
- [ ] T018 Verify the floating blue bubble appears at the bottom-right of the Docusaurus site.
- [ ] T019 Verify the chat widget opens and closes correctly.
- [ ] T020 Test basic chat interaction (sending messages, receiving responses) using the locally running backend.
- [ ] T021 Verify the widget's appearance in Docusaurus dark mode.
- [ ] T022 Test responsiveness and layout on mobile screen sizes.
- [ ] T023 Simulate offline mode (e.g., by disabling network) and verify "no connection" message.

**Checkpoint**: At this point, User Stories 1 AND 2 should both work independently.

---

## Phase 5: Polish & Cross-Cutting Concerns

**Purpose**: Prepare for deployment and ensure overall quality and compliance.

- [ ] T024 Review all code against constitutional principles (e.g., no third-party trackers, key exposure).
- [ ] T025 Create deployment instructions for the RAG backend to Vercel (or similar free-tier platform).
- [ ] T026 Update `API_URL` in `ai-robotics-mini-book/src/components/AIChat/index.js` to the live Vercel backend URL after deployment.
- [ ] T027 Conduct end-to-end testing of the integrated system in a deployed environment.

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately
- **Foundational (Phase 2)**: Depends on Setup completion - BLOCKS all user stories
- **User Stories (Phase 3+)**: All depend on Foundational phase completion
  - User stories can then proceed in parallel (if staffed)
  - Or sequentially in priority order (P1 → P2)
- **Polish (Phase 5)**: Depends on all desired user stories being complete

### User Story Dependencies

- **User Story 1 (P1)**: Can start after Foundational (Phase 2) - No dependencies on other stories
- **User Story 2 (P2)**: Can start after Foundational (Phase 2) - Integrates with US1's backend.

### Within Each User Story

- Core implementation before integration.
- Story complete before moving to next priority.

### Parallel Opportunities

- Within each phase, tasks without explicit dependencies can be executed in parallel.
- Once Foundational phase completes, User Story 1 and User Story 2 can conceptually be worked on by different teams, with US2 depending on US1's backend API.

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Phase 1: Setup
2. Complete Phase 2: Foundational (CRITICAL - blocks all stories)
3. Complete Phase 3: User Story 1
4. **STOP and VALIDATE**: Test User Story 1 independently.
5. Deploy/demo if ready.

### Incremental Delivery

1. Complete Setup + Foundational → Foundation ready
2. Add User Story 1 → Test independently → Deploy/Demo (RAG backend functional)
3. Add User Story 2 → Test independently → Deploy/Demo (Chat widget integrated and functional)
4. Each story adds value without breaking previous stories.

### Parallel Team Strategy

With multiple developers:

1. Team completes Setup + Foundational together.
2. Once Foundational is done:
   - Developer A: User Story 1 (Backend development)
   - Developer B: User Story 2 (Frontend development, integrating with A's local/dev backend)
3. Stories complete and integrate.

---

## Notes

- Verify tests fail before implementing.
- Commit after each task or logical group.
- Stop at any checkpoint to validate story independently.
- Avoid: vague tasks, same file conflicts, cross-story dependencies that break independence.
