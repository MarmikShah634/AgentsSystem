---
id: write-tsd-overview
category: tsd
owner_agent: tech-spec-author
inputs:
  - prd_path
  - architecture
outputs:
  - section
requires_plan: true
emits_confidence: true
---

# Skill: write-tsd-overview

## Task

Write the TSD overview: 1 paragraph restating the PRD goals in technical
terms + a bullet list of components touched + cross-link to PRD section
ids.

## Stop condition

Every PRD goal is referenced by id; every component named appears in the
architecture doc.
