---
id: check-prd-testability
category: prd
owner_agent: prd-reviewer
inputs:
  - prd_path
outputs:
  - findings
requires_plan: true
emits_confidence: true
---

# Skill: check-prd-testability

## Task

Each FR and NFR must be testable. Flag any that:

- Uses adjectives without numbers ("fast", "intuitive").
- Lacks an observable trigger.
- Refers to internal state with no external symptom.

## Stop condition

Findings list every untestable requirement with a concrete rewrite.
