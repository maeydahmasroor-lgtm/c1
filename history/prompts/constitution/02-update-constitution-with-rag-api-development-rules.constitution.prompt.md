---
id: 02
title: Update Constitution with RAG API Development Rules
stage: constitution
date: 2026-01-02
surface: agent
model: gemini-pro
feature: rag-api
branch: main
user: Adminstrator
command: /sp.constitution
labels: [constitution, rag, api]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files:
  - .specify/memory/constitution.md
tests:
  null
---

## Prompt

/sp.constitution You are an expert Python developer building a production-ready RAG API with FastAPI and Qdrant. Rules:
- Use FastAPI for REST endpoints (/ingest, /chat).
- Use Qdrant (local or cloud) as vector DB with collection "book_collection".
- Embed with Gemini embedding-001 via LangChain.
- Generate answers with gemini-1.5-flash.
- Always count tokens using genai.count_tokens before generation; truncate context if total > 800_000 tokens.
- Load env vars with python-dotenv.
- Write clean, modular, type-annotated code with error handling.
- Optimize prompts and context for minimal token usage.

## Response snapshot

The project constitution has been updated to version 3.0.0 to reflect the new development principles for the RAG API. The core principles now detail the use of FastAPI, Qdrant, Gemini models for embedding and generation, token counting, environment variable management, and code quality standards.

## Outcome

- ✅ Impact: Major update to the project's guiding principles.
- 🧪 Tests: n/a
- 📁 Files: 1 modified
- 🔁 Next prompts: The user can now proceed with development based on the new constitution.
- 🧠 Reflection: The constitution was successfully updated to align with the new, more specific project requirements.

## Evaluation notes (flywheel)

- Failure modes observed: None
- Graders run and results (PASS/FAIL): PASS
- Prompt variant (if applicable): null
- Next experiment (smallest change to try): n/a
