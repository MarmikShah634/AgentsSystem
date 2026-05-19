---
id: assemble-tsd
category: tsd
owner_agent: tech-spec-author
inputs:
  - sections
  - slug
outputs:
  - tsd_path
requires_plan: true
emits_confidence: true
---

# Skill: assemble-tsd

## Task

Stitch sections into `docs/tsd/<slug>.md` in this fixed order:

1. Overview
2. Component Contracts
3. Data Contracts
4. API Contracts
5. Error Model
6. Observability
7. Rollout Plan

## Stop condition

All seven headings present; no `<...>` placeholders; PRD cross-links
resolve.
