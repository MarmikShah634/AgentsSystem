---
id: assign-sprint-goals
category: sprint
owner_agent: sprint-planner
inputs:
  - sprints
outputs:
  - sprint_goals
requires_plan: true
emits_confidence: true
---

# Skill: assign-sprint-goals

## Task

Write one sentence per sprint stating what is shippable at end-of-sprint
that wasn't before. No vague goals ("make progress on X"), no
multi-clause goals joined by "and".

## Stop condition

Every sprint has exactly one single-clause goal.
