# ADR-1: Embedding Model and LLM Provider Choice

> **Scope**: Document decision clusters, not individual technology choices. Group related decisions that work together (e.g., "Frontend Stack" not separate ADRs for framework, styling, deployment).

- **Status:** Proposed
- **Date:** 2026-01-03
- **Feature:** 003-chatbot-backend
- **Context:** The project constitution specifies using `Gemini embedding-001` for embeddings and `gemini-1.5-flash` for LLM responses. However, the initial project setup and dependencies for the `chatbot-backend` feature suggest the use of `FastEmbed` and the inclusion of `OpenAI` as an additional LLM provider. This ADR documents the decision to deviate from the constitution to accommodate these project-specific requirements.

<!-- Significance checklist (ALL must be true to justify this ADR)
     1) Impact: Long-term consequence for architecture/platform/security?
     2) Alternatives: Multiple viable options considered with tradeoffs?
     3) Scope: Cross-cutting concern (not an isolated detail)?
     If any are false, prefer capturing as a PHR note instead of an ADR. -->

## Decision

- **Embedding Model**: Use `FastEmbed` for generating text embeddings.
- **LLM Providers**: Support both `OpenAI` and `gemini-1.5-flash` for generating chat responses, allowing for flexibility and comparison.

<!-- For technology stacks, list all components:
     - Framework: Next.js 14 (App Router)
     - Styling: Tailwind CSS v3
     - Deployment: Vercel
     - State Management: React Context (start simple)
-->

## Consequences

### Positive

- `FastEmbed` may offer better performance, offline capabilities, or lower costs compared to the Gemini embedding model.
- Supporting multiple LLM providers allows for greater flexibility, enabling the system to leverage the strengths of different models or to switch providers based on cost, performance, or availability.

### Negative

- Deviates from the project constitution, potentially leading to inconsistencies across different project features.
- Increases complexity by requiring the system to handle different APIs and models.
- May require additional configuration and maintenance to manage multiple providers.

## Alternatives Considered

- **Strict Adherence to Constitution**: Use only `Gemini embedding-001` and `gemini-1.5-flash`. This was rejected because it would require removing existing dependencies (`FastEmbed`, `openai`) from the `chatbot-backend` project, which appear to be deliberate choices. It would also remove the flexibility of using multiple LLM providers.

## References

- Feature Spec: `specs/003-chatbot-backend/spec.md`
- Implementation Plan: `specs/003-chatbot-backend/plan.md`
- Related ADRs: None
- Evaluator Evidence: None
