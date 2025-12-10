---
id: 02
title: Update Constitution with 10 Principles
stage: constitution
date: 2025-12-10
surface: agent
model: gemini-pro
feature: none
branch: {{BRANCH}}
user: {{USER}}
command: /sp.constitution
labels: [constitution, update]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files:
- .specify/memory/constitution.md
tests:
- none
---

## Prompt

/sp.constitution ### sp.specify → CONSTITUTION (final, short, unbreakable)

1. Answers come ONLY from the book’s own text. Anything else = “I don’t know”.  
2. Selected/highlighted text is the highest authority.  
3. No third-party widgets, trackers, analytics, or chat services. Ever.  
4. google api key.  
5. Must run forever on free tiers (Qdrant Free).  
6. Exactly one blue floating bubble (bottom-right). Nothing else floats.  
7. Works on mobile and instantly follows Docusaurus dark mode.  
8. Widget loads and opens even offline (just shows “no connection”).  
9. Full deploy from zero in ≤ 60 minutes.  
10. Remove the chatbot tomorrow → book still 100 % perfect.

10 rules. No exceptions.  
Ratified 10 Dec 2025.

## Response snapshot

I have updated the constitution with the 10 principles you provided. I also updated the version of the constitution to 1.1.0 and the last amended date to 2025-12-10.

## Outcome

- ✅ Impact: The project constitution has been updated with 10 new principles.
- 🧪 Tests: No tests were run.
- 📁 Files: .specify/memory/constitution.md was modified.
- 🔁 Next prompts: none
- 🧠 Reflection: The initial attempt to create the PHR using the shell script failed. I was able to recover by using the fallback method of reading the template and creating the file manually.

## Evaluation notes (flywheel)

- Failure modes observed: The shell script to create the PHR was not found.
- Graders run and results (PASS/FAIL): none
- Prompt variant (if applicable): none
- Next experiment (smallest change to try): none
