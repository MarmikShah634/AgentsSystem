---
id: write-error-model
category: tsd
owner_agent: tech-spec-author
inputs:
  - functional_requirements
outputs:
  - section
requires_plan: true
emits_confidence: true
---

# Skill: write-error-model

## Task

A taxonomy of all error classes with:

- Code (stable identifier, e.g. `AUTH_EXPIRED`).
- HTTP status (where applicable).
- User-facing message (or null if internal).
- When raised.
- Recovery path (retry / refresh / give up).

## Stop condition

Every error has all five fields; no duplicate codes.
