---
id: enforce-test-pairing
category: infra
owner_agent: infra-planner
inputs:
  - steps
outputs: []
requires_plan: false
emits_confidence: false
---

# Skill: enforce-test-pairing

Raise `PlanInvariantError` if any `frontend`/`backend` step lacks a paired
`testing/*` step in `test_pair`.
