# Data Model for Chatbot Backend

**Branch**: `003-chatbot-backend` | **Date**: 2026-01-02

This document defines the data models for the Chatbot Backend, based on the requirements in `spec.md`.

## Core Entities

### 1. ChatRequest

Represents an incoming chat message from a user.

- **Fields**:
  - `user_id`: `string` (Optional) - A unique identifier for the user.
  - `message`: `string` - The text of the user's message.
  - `session_id`: `string` (Optional) - A unique identifier for the chat session.

### 2. ChatResponse

Represents a response from the chatbot.

- **Fields**:
  - `response`: `string` - The text of the chatbot's generated response.
  - `sources`: `List[Source]` (Optional) - A list of sources used to generate the response.

### 3. Source

Represents a single source document retrieved from the vector store.

- **Fields**:
  - `document_id`: `string` - The unique identifier of the source document.
  - `content`: `string` - A snippet of the source content.
  - `score`: `float` - The relevance score of the source.

## State Transitions

The primary state transition is from a `ChatRequest` to a `ChatResponse`. The application logic will handle this transformation by orchestrating calls to the vector store and the LLM.
