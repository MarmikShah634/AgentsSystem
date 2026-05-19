---
id: sequence-dependencies
category: planning
owner_agent: planner
inputs:
  - plan_steps
outputs:
  - ordered_steps
requires_plan: false
emits_confidence: true
---

# Skill: sequence-dependencies

## Task

Topologically order plan steps. Fail if a cycle is detected.
