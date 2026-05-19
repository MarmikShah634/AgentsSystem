---
id: build-plan
category: infra
owner_agent: infra-planner
inputs:
  - goal
  - owner_agent
  - steps
outputs:
  - plan
requires_plan: false
emits_confidence: false
---

# Skill: build-plan

Wrap `steps` in the canonical plan envelope, run `enforce-test-pairing`,
then persist via `infra-logger.save-plan`.
