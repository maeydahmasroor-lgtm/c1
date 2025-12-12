# Research for Docusaurus Chatbot

This document addresses the "NEEDS CLARIFICATION" items from the implementation plan.

## 1. Book Content Source Format

- **Decision**: The book content will be sourced from the existing Markdown (`.md` and `.mdx`) files within the `ai-robotics-mini-book/docs` directory.
- **Rationale**: The `spec.md` mentions the chatbot should use the "Physical AI & Humanoid Robotics book as provided in docusasrus based book". The existing Docusaurus site is built from these Markdown files. A data ingestion script will be created to parse these files, chunk the text, generate embeddings, and store them in Qdrant.

## 2. Chat Interface Integration

- **Decision**: The chat interface will be a floating action button in the bottom-right corner of the screen, available on all pages. Clicking it will open the chat window.
- **Rationale**: This approach, common for support chatbots, is minimally intrusive and provides consistent access to the chatbot across the entire site without altering the existing layout of content pages.

## 3. Performance Requirements

- **Decision**: A performance goal of **p95 response time under 3 seconds** will be adopted.
- **Rationale**: This is a reasonable starting point for a good user experience. This includes the time from the user sending a message to the first part of the response appearing in the UI. This will be measured and optimized during development.

## 4. Docusaurus `Root.js` Swizzling

- **Decision**: The Docusaurus `Root` component will be "swizzled" to wrap the application in a context provider for the chatbot state.
- **Command**: `npm run swizzle @docusaurus/theme-classic Root -- --eject`
- **Rationale**: Swizzling is the official Docusaurus method for replacing or wrapping theme components. By wrapping `Root`, we can maintain a global state for the chatbot (e.g., its visibility, conversation history) that persists across page navigations.

## 5. FastAPI Backend Structure

- **Decision**: The backend will follow a standard service-oriented structure as outlined in the `plan.md`.
- **Rationale**: This structure separates concerns, making the application easier to develop, test, and maintain.
  - `api/`: FastAPI routers and endpoints.
  - `core/`: Configuration and settings management.
  - `models/`: Pydantic for API models, SQLAlchemy for DB models.
  - `services/`: Business logic for interacting with OpenAI and Qdrant.
  - `data/`: Scripts for one-time data ingestion.

## 6. SQLite Database Schema

- **Decision**: A simple schema for storing conversation history.
- **Rationale**: This allows for future features like displaying past conversations to the user.
  - **`conversations` table**:
    - `id` (PK, UUID)
    - `created_at` (Timestamp)
  - **`messages` table**:
    - `id` (PK, UUID)
    - `conversation_id` (FK to `conversations.id`)
    - `role` (Enum: 'user', 'assistant')
    - `content` (Text)
    - `created_at` (Timestamp)

## 7. OpenAI API Key Management

- **Decision**: The OpenAI API key will be managed via an environment variable (`OPENAI_API_KEY`). The backend will load this variable using a library like `python-dotenv` for local development.
- **Rationale**: This is a standard, secure practice that avoids hardcoding secrets in the source code. The `.env` file will be added to `.gitignore`.

## 8. Qdrant Client Configuration

- **Decision**: The Qdrant client will be configured to connect to a local Qdrant instance running in Docker for development, and configurable via environment variables for production (e.g., Qdrant Cloud).
- **Rationale**: This provides a free and easy-to-manage local development setup while allowing for a seamless transition to a managed cloud solution for production. We will provide a `docker-compose.yml` for setting up Qdrant locally.

## 9. `uv` Virtual Environment Setup

- **Decision**: `uv` will be used to create and manage the virtual environment.
- **Commands**:
  - `uv venv` (to create the `.venv` directory)
  - `uv pip install -r requirements.txt` (to install dependencies)
- **Rationale**: `uv` is a modern, fast tool for Python packaging that simplifies environment management.
