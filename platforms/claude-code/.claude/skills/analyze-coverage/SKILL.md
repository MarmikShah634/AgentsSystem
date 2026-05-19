---
id: analyze-coverage
category: testing
owner_agent: tester
inputs:
  - coverage_report_path
outputs:
  - coverage_summary
requires_plan: true
emits_confidence: true
---

# Skill: analyze-coverage

## Task

Parse the coverage report (lcov/coverage.json/etc.) and emit per-file
line/branch coverage. Flag any file below 70% as `needs_attention`.
