---
id: code-review
category: review
owner_agent: reviewer
inputs:
  - patch
  - acceptance_criteria
outputs:
  - findings
requires_plan: true
emits_confidence: true
---

# Skill: code-review

## Task

Review the patch for correctness against acceptance criteria, simplicity,
and consistency with existing code. Do NOT rewrite — report findings only.

## Output

`{findings: [{severity, path, line, msg}], verdict: pass|changes-requested|block}`
