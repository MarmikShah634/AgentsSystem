---
id: extract-acceptance-criteria
category: requirements
owner_agent: requirements
inputs:
  - user_stories
outputs:
  - acceptance_criteria
requires_plan: false
emits_confidence: true
---

# Skill: extract-acceptance-criteria

## Task

For each user story, write 1..N Given/When/Then acceptance criteria.

## Stop condition

Every story has at least one G/W/T entry covering the happy path AND at
least one edge case (empty input, auth failure, etc.).
