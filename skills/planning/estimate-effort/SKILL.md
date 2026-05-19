---
id: estimate-effort
category: planning
owner_agent: planner
inputs:
  - plan_steps
outputs:
  - effort_estimate
requires_plan: false
emits_confidence: true
---

# Skill: estimate-effort

## Task

Assign a t-shirt size (XS/S/M/L/XL) to each plan step. Sum to a total.

## Output

```json
{"per_step": {"<step_id>": "S"}, "total": "M"}
```
