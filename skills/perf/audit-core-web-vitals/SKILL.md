---
id: audit-core-web-vitals
category: perf
owner_agent: performance-auditor
inputs:
  - puppeteer_run
  - budgets
outputs:
  - findings
requires_plan: true
emits_confidence: true
---

# Skill: audit-core-web-vitals

## Task

Collect LCP, INP, CLS, TTFB from a Puppeteer run. Compare to budgets
(default: LCP ≤ 2.5s, INP ≤ 200ms, CLS ≤ 0.1, TTFB ≤ 800ms). Flag any
metric over budget with the affected URL.
