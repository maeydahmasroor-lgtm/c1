# Research for Chatbot Backend

**Branch**: `003-chatbot-backend` | **Date**: 2026-01-02

This document outlines the research tasks identified during the planning phase for the Chatbot Backend feature.

## Phase 0: Research Tasks

### 1. Resolve "NEEDS CLARIFICATION" items

- **Testing Strategy:**
  - **Task:** Define the testing strategy.
  - **Details:** Research and decide on the best practices for testing a FastAPI application. Confirm if `pytest` is the right choice and define the structure for unit and integration tests.

- **Performance Goals:**
  - **Task:** Define specific and measurable performance goals.
  - **Details:** Determine the expected load and define targets for key metrics like response time (e.g., p95, p99) and requests per second.

- **Constraints:**
  - **Task:** Define operational and technical constraints.
  - **Details:** Identify any limitations, such as memory usage, concurrent user limits, or API rate limits from external services.

- **Scale & Scope:**
  - **Task:** Define the scale and scope of the initial implementation.
  - **Details:** Clarify the target number of users, a volume of data to be handled, and the specific features to be included in the first version.

- **Token Counting:**
  - **Task:** Define the token counting and context truncation strategy.
  - **Details:** Specify how token counting will be implemented (e.g., which library to use) and the exact logic for truncating context to stay within model limits, as per Constitution Principle #5.

### 2. Resolve Constitution Violations

- **Embedding Model (`FastEmbed` vs. `Gemini embedding-001`):**
  - **Task:** Justify or rectify the choice of an embedding model.
  - **Details:** Investigate the reasons for using `FastEmbed` as specified in the `pyproject.toml`. Compare its performance, cost, and features against the constitution's requirement of `Gemini embedding-001`. Propose a final decision with a clear rationale.

- **LLM Provider (`OpenAI`):**
  - **Task:** Justify or rectify the inclusion of `OpenAI` as an LLM provider.
  - **Details:** Clarify the purpose of having both `OpenAI` and `Google Genai`. If both are needed, the constitution should be amended. If not, the unused dependency should be removed.

## Phase 1: Design & Contracts

The findings from this research will inform the creation of the `data-model.md`, API contracts, and `quickstart.md`.
