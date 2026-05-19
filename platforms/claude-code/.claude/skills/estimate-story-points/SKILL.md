---
id: estimate-story-points
category: sprint
owner_agent: sprint-planner
inputs:
  - stories
outputs:
  - estimates
requires_plan: true
emits_confidence: true
---

# Skill: estimate-story-points

## Task

Assign Fibonacci points (1, 2, 3, 5, 8, 13) per story. Document the
reference story for each point value. No story may exceed 13 — split it
first.

## Stop condition

Every story has a point value; reference story map is included.
