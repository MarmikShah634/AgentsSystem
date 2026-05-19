---
id: check-tsd-implementability
category: tsd
owner_agent: tech-spec-reviewer
inputs:
  - tsd_path
outputs:
  - findings
requires_plan: true
emits_confidence: true
---

# Skill: check-tsd-implementability

## Task

For each component contract, decide if a coding agent could implement it
from the text alone. Flag any spec that:

- Mentions a library/API not in the architecture doc.
- Has a method without a signature.
- Has a failure mode without a recovery rule.
