# Data Models for Docusaurus Chatbot

This document defines the data models for the components of the chatbot system.

## 1. Qdrant Vector Store Model

The vector store will hold the content of the book, chunked into searchable pieces.

- **Collection Name**: `docusaurus_book`
- **Vector Parameters**:
  - `size`: 1536 (for OpenAI's `text-embedding-ada-002` model)
  - `distance`: Cosine
- **Point (Vector) Payload**:
  - `text` (string): The actual text chunk from the book.
  - `source` (string): The path to the source Markdown file (e.g., `docs/chapter-01.md`).
  - `metadata` (object, optional): Any other relevant metadata, like chapter title or section.

## 2. SQLite Relational Database Models

The SQLite database will store conversation history.

### `conversations` Table

Represents a single conversation session.

| Column | Type | Constraints | Description |
|---|---|---|---|
| `id` | TEXT | PRIMARY KEY, NOT NULL | A unique identifier (UUID) for the conversation. |
| `created_at` | DATETIME | NOT NULL, DEFAULT CURRENT_TIMESTAMP | The timestamp when the conversation was created. |

### `messages` Table

Represents a single message within a conversation.

| Column | Type | Constraints | Description |
|---|---|---|---|
| `id` | TEXT | PRIMARY KEY, NOT NULL | A unique identifier (UUID) for the message. |
| `conversation_id` | TEXT | NOT NULL, FOREIGN KEY (`conversations.id`) | The ID of the conversation this message belongs to. |
| `role` | TEXT | NOT NULL, CHECK(`role` IN ('user', 'assistant')) | The role of the message sender. |
| `content` | TEXT | NOT NULL | The text content of the message. |
| `created_at` | DATETIME | NOT NULL, DEFAULT CURRENT_TIMESTAMP | The timestamp when the message was created. |
