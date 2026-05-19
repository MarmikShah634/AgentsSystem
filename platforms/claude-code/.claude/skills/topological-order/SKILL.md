---
id: topological-order
category: infra
owner_agent: infra-planner
inputs:
  - steps
outputs:
  - ordered_steps
requires_plan: false
emits_confidence: false
---

# Skill: topological-order

Topologically order `steps` by `depends_on`. Raise `PlanInvariantError`
on cycle.
