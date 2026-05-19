---
id: validate-requirements
category: requirements
owner_agent: requirements
inputs:
  - user_stories
  - acceptance_criteria
outputs:
  - validation_report
requires_plan: false
emits_confidence: true
---

# Skill: validate-requirements

## Task

Check the requirements doc for: completeness (every story has criteria),
testability (every criterion is observable), and non-contradiction.

## Output

```json
{ "issues": [{"story_id": "...", "kind": "...", "msg": "..."}],
  "verdict": "pass|revise" }
```
