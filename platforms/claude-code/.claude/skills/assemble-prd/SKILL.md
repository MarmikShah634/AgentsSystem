---
id: assemble-prd
category: prd
owner_agent: prd-author
inputs:
  - sections
  - slug
outputs:
  - prd_path
requires_plan: true
emits_confidence: true
---

# Skill: assemble-prd

## Task

Stitch the section drafts into `docs/prd/<slug>.md` in this fixed order:

1. Executive Summary
2. Problem Statement
3. Goals & Non-Goals
4. User Personas
5. Functional Requirements
6. Non-Functional Requirements
7. Success Metrics
8. Out of Scope
9. Open Questions

## Stop condition

All nine headings present; file parses as valid Markdown; no unresolved
`<...>` placeholders.
