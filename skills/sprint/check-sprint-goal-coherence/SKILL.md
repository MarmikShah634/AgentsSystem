---
id: check-sprint-goal-coherence
category: sprint
owner_agent: sprint-reviewer
inputs:
  - sprints
outputs:
  - findings
requires_plan: true
emits_confidence: true
---

# Skill: check-sprint-goal-coherence

## Task

Flag a sprint when its goal does not describe a deliverable, or when
≥30% of the sprint's stories don't contribute to the stated goal.
