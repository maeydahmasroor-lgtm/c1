---
id: 004
title: Generate Tasks for Chatbot Feature
stage: plan
date: 2025-12-10
surface: agent
model: gemini
feature: 001-constitution-principles
branch: 001-constitution-principles
user: Adminstrator
command: /sp.tasks
labels: ["tasks-generation", "plan"]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files:
  - specs/001-constitution-principles/tasks.md
tests:
  - null
---

## Prompt

description: Generate an actionable, dependency-ordered tasks.md for the feature based on available design artifacts.


## User Input

```text
$ARGUMENTS
```

You **MUST** consider the user input before proceeding (if not empty).

## Outline

1. **Setup**: Run `.specify/scripts/powershell/check-prerequisites.ps1 -Json` from repo root and parse FEATURE_DIR and AVAILABLE_DOCS list. All paths must be absolute. For single quotes in args like "I'm Groot", use escape syntax: e.g 'I'\''m Groot' (or double-quote if possible: "I'm Groot").

2. **Load design documents**: Read from FEATURE_DIR:
   - **Required**: plan.md (tech stack, libraries, structure), spec.md (user stories with priorities)
   - **Optional**: data-model.md (entities), contracts/ (API endpoints), research.md (decisions), quickstart.md (test scenarios)
   - Note: Not all projects have all documents. Generate tasks based on what's available.

3. **Execute task generation workflow**:
   - Load plan.md and extract tech stack, libraries, project structure
   - Load spec.md and extract user stories with their priorities (P1, P2, P3, etc.)
   - If data-model.md exists: Extract entities and map to user stories
   - If contracts/ exists: Map endpoints to user stories
   - If research.md exists: Extract decisions for setup tasks
   - Generate tasks organized by user story (see Task Generation Rules below)
   - Generate dependency graph showing user story completion order
   - Create parallel execution examples per user story
   - Validate task completeness (each user story has all needed tasks, independently testable)

4. **Generate tasks.md**: Use `.specify.specify/templates/tasks-template.md` as structure, fill with:
   - Correct feature name from plan.md
   - Phase 1: Setup tasks (project initialization)
   - Phase 2: Foundational tasks (blocking prerequisites for all user stories)
   - Phase 3+: One phase per user story (in priority order from spec.md)
   - Each phase includes: story goal, independent test criteria, tests (if requested), implementation tasks
   - Final Phase: Polish & cross-cutting concerns
   - All tasks must follow the strict checklist format (see Task Generation Rules below)
   - Clear file paths for each task
   - Dependencies section showing user story completion order
   - Parallel execution examples per story
   - Implementation strategy section (MVP first, incremental delivery)

5. **Report**: Output path to generated tasks.md and summary:
   - Total task count
   - Task count per user story
   - Parallel opportunities identified
   - Independent test criteria for each story
   - Suggested MVP scope (typically just User Story 1)
   - Format validation: Confirm ALL tasks follow the checklist format (checkbox, ID, labels, file paths)

Context for task generation: there is no fourth key it was said by mistake


## Response snapshot

Generated `tasks.md` located at `specs/001-constitution-principles/tasks.md` based on `plan.md`, `spec.md`, and provided code snippets.

## Outcome

- ✅ Impact: Generated a detailed, actionable `tasks.md` for the chatbot feature.
- 🧪 Tests: No explicit test generation was requested.
- 📁 Files: `specs/001-constitution-principles/tasks.md` created.
- 🔁 Next prompts: Next is implementation based on the `tasks.md`.
- 🧠 Reflection: The clarification of missing code and the `.env` keys was crucial for task generation. The issue with `create-phr.sh` highlighted the need for agent-native PHR creation in PowerShell environment.

## Evaluation notes (flywheel)

- Failure modes observed: Attempted to run bash script in PowerShell environment.
- Graders run and results (PASS/FAIL): N/A
- Prompt variant (if applicable): N/A
- Next experiment (smallest change to try): N/A
