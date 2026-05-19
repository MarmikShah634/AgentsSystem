---
id: score-sprint-plan-quality
category: sprint
owner_agent: sprint-reviewer
inputs:
  - findings
outputs:
  - readiness_score
  - verdict
requires_plan: true
emits_confidence: true
---

# Skill: score-sprint-plan-quality

## Task

Aggregate sprint findings into 0.0–1.0.

```
score = 1.0
  - 0.20 per cyclic dependency
  - 0.15 per over-committed sprint
  - 0.10 per incoherent goal
verdict = "pass" if score >= 0.85 else "revise"
```
