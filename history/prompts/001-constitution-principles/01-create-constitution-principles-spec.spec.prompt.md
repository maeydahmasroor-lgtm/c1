---
id: 01
title: Create Constitution Principles Spec
stage: spec
date: 2025-12-10
surface: agent
model: (unknown)
feature: 001-constitution-principles
branch: (not applicable, as user opted out of git)
user: (unknown)
command: /sp.specify "### sp.specify → CONSTITUTION (final, short, unbreakable) 1. Answers come ONLY from the book’s own text. Anything else = “I don’t know”. 2. Selected/highlighted text is the highest authority. 3. No third-party widgets, trackers, analytics, or chat services. Ever. 4. OpenAI key never reaches the browser. 5. Must run forever on free tiers (Qdrant Free, Vercel Hobby, OpenAI pay-as-you-go). 6. Exactly one blue floating bubble (bottom-right). Nothing else floats. 7. Works on mobile and instantly follows Docusaurus dark mode. 8. Widget loads and opens even offline (just shows “no connection”). 9. Full deploy from zero in ≤ 60 minutes. 10. Remove the chatbot tomorrow → book still 100 % perfect. 10 rules. No exceptions. Ratified 10 Dec 2025.### sp.specify → CONSTITUTION (final, short, unbreakable) 1. Answers come ONLY from the book’s own text. Anything else = “I don’t know”. 2. Selected/highlighted text is the highest authority. 3. No third-party widgets, trackers, analytics, or chat services. Ever. 4. gemini key never reaches the browser. 5. Must run forever on free tiers (Qdrant Free). 6. Exactly one blue floating bubble (bottom-right). Nothing else floats. 7. Works on mobile and instantly follows Docusaurus dark mode. 8. Widget loads and opens even offline (just shows “no connection”)."
labels: ["specification", "constitution", "principles"]
links:
  spec: specs/001-constitution-principles/spec.md
  ticket: null
  adr: null
  pr: null
files:
  - specs/001-constitution-principles/spec.md
  - specs/001-constitution-principles/checklists/requirements.md
tests:
  - 
---

## Prompt

### sp.specify → CONSTITUTION (final, short, unbreakable) 1. Answers come ONLY from the book’s own text. Anything else = “I don’t know”. 2. Selected/highlighted text is the highest authority. 3. No third-party widgets, trackers, analytics, or chat services. Ever. 4. OpenAI key never reaches the browser. 5. Must run forever on free tiers (Qdrant Free, Vercel Hobby, OpenAI pay-as-you-go). 6. Exactly one blue floating bubble (bottom-right). Nothing else floats. 7. Works on mobile and instantly follows Docusaurus dark mode. 8. Widget loads and opens even offline (just shows “no connection”). 9. Full deploy from zero in ≤ 60 minutes. 10. Remove the chatbot tomorrow → book still 100 % perfect. 10 rules. No exceptions. Ratified 10 Dec 2025.### sp.specify → CONSTITUTION (final, short, unbreakable) 1. Answers come ONLY from the book’s own text. Anything else = “I don’t know”. 2. Selected/highlighted text is the highest authority. 3. No third-party widgets, trackers, analytics, or chat services. Ever. 4. gemini key never reaches the browser. 5. Must run forever on free tiers (Qdrant Free). 6. Exactly one blue floating bubble (bottom-right). Nothing else floats. 7. Works on mobile and instantly follows Docusaurus dark mode. 8. Widget loads and opens even offline (just shows “no connection”).

## Response snapshot

Created feature specification and checklist for 'Constitution Principles'. Spec is ready for planning.

## Outcome

- ✅ Impact: Successfully created the feature specification and quality checklist based on the provided constitution rules. The spec is ready for the planning phase.
- 🧪 Tests: No automated tests were run for this stage.
- 📁 Files: Created `specs/001-constitution-principles/spec.md` and `specs/001-constitution-principles/checklists/requirements.md`.
- 🔁 Next prompts: Proceed to `/sp.plan` to create a plan for implementing the 'Constitution Principles'.
- 🧠 Reflection: Initial issues with `create-new-feature.ps1` due to argument parsing, resolved by adapting to tool's parsing limitations and user's git opt-out. The specification itself had to be creatively adapted from a set of constitution rules. One checklist item (Dependencies and Assumptions) required a spec update.

## Evaluation notes (flywheel)

- Failure modes observed: Command parsing issues with `run_shell_command` due to long string content. Ambiguity in `create-new-feature.ps1` arguments.
- Graders run and results (PASS/FAIL): (N/A)
- Prompt variant (if applicable): (N/A)
- Next experiment (smallest change to try): (N/A)
