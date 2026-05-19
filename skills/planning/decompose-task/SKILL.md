---
id: decompose-task
category: planning
owner_agent: planner
inputs:
  - requirements
  - architecture
outputs:
  - plan_steps
requires_plan: false
emits_confidence: true
---

# Skill: decompose-task

## Task

Break the goal into ordered plan steps. Each step references exactly one
skill and one agent.

## Invariants

- Every `coding/*` step has a paired `testing/*` step (`test_pair`).
- Steps have explicit `depends_on`.
- Sensitive-surface steps set `human_gate: true`.
