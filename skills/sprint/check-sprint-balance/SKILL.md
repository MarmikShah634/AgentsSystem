---
id: check-sprint-balance
category: sprint
owner_agent: sprint-reviewer
inputs:
  - sprints
  - velocity
outputs:
  - findings
requires_plan: true
emits_confidence: true
---

# Skill: check-sprint-balance

## Task

Flag sprints that are:

- Over-committed (points > velocity).
- Under-committed (points < 0.6 × velocity).
- Dominated by one risky story (single story > 50% of sprint).
