---
id: group-prd-into-epics
category: sprint
owner_agent: sprint-planner
inputs:
  - prd_path
outputs:
  - epics
requires_plan: true
emits_confidence: true
---

# Skill: group-prd-into-epics

## Task

Cluster PRD FRs into 3–8 epics. Each epic must:

- Map to one persona or one workflow.
- Have a name in noun form ("Auth", "Checkout").
- List its constituent FR ids.

## Stop condition

Every FR appears in exactly one epic.
