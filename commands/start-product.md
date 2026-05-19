---
id: start-product
description: "Run the full product lifecycle: PRD → TSD → sprints → code → ship"
entry_agent: requirements
---

# /start-product

**Usage:** `/start-product <one-liner>`

The full pipeline. Each arrow is a confidence-gated hand-off.

```
requirements         (gather raw stakeholder input)
   ↓
prd-author           (write PRD section-by-section)
   ↓
prd-reviewer         (gap-check PRD; ≥0.85 readiness to pass)
   ↓
architect            (tech stack + components + data model)
   ↓
tech-spec-author     (write TSD section-by-section)
   ↓
tech-spec-reviewer   (gap-check TSD; ≥0.90 readiness to pass)
   ↓
sprint-planner       (epics → stories → estimates → sprints → goals)
   ↓
sprint-reviewer      (gap-check sprint plan; ≥0.85 readiness)
   ↓
planner              (per-sprint task decomposition)
   ↓
designer + frontend + backend     (per-task)
   ↓
tester (unit + Puppeteer)
   ↓
accessibility-auditor + performance-auditor   (UI surfaces)
   ↓
reviewer + security
   ↓
docs + devops + deployer
```

Each agent's outputs land in `docs/{prd,tsd,sprints}/<slug>.{md,yaml}`
and `logs/plans/`. Audit records flow to `logs/audit/<date>.jsonl`.
