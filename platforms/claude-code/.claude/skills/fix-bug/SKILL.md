---
id: fix-bug
category: coding
owner_agent: coder
inputs:
  - bug_report
  - failing_test
outputs:
  - patch
requires_plan: true
emits_confidence: true
---

# Skill: fix-bug

## Task

Make `failing_test` pass with the minimum diff. Do NOT add unrelated tests
or refactors. The failing test must exist BEFORE the fix — the planner
ensures this by emitting a `generate-regression-test` step first.

## Stop condition

`failing_test` passes; all previously-green tests remain green.
