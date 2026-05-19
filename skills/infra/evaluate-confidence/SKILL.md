---
id: evaluate-confidence
category: infra
owner_agent: infra-confidence
inputs:
  - confidence
  - touched_paths
outputs:
  - decision
requires_plan: false
emits_confidence: false
---

# Skill: evaluate-confidence

Return `{allowed, reason, needs_human}` given the agent's confidence
score and the set of touched paths.

Floor: 0.90. Sensitive globs: see `agents/infra-confidence.md`.
