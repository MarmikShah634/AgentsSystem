---
id: start-feature
description: "Add a feature to an existing product (assumes PRD/TSD exist)"
entry_agent: planner
---

# /start-feature

**Usage:** `/start-feature <goal>`

Single-feature flow for projects that already have a validated PRD and
TSD. For a brand-new product, use `/start-product` instead — it runs the
full PRD-first lifecycle.

## Preconditions

- `docs/prd/<slug>.md` exists and has been verdict-passed by `prd-reviewer`.
- `docs/tsd/<slug>.md` exists and has been verdict-passed by `tech-spec-reviewer`.
- The architecture has not changed since the TSD was approved.

If any of the above is missing, STOP and route to `/start-product`.

## Sequence

1. `architect` → `select-tech-stack` — confirm the existing stack still
   covers the new feature; flag any new dependency for human gate.
2. `sprint-planner` → `group-prd-into-epics` → `decompose-epic-into-stories`
   → `estimate-story-points` → `sequence-sprints` → `assign-sprint-goals`
   — emits a 1-sprint plan scoped to the feature. (If the feature would
   need more than one sprint, this command exits with `revise` and asks
   the human to switch to `/start-product`.)
3. `sprint-reviewer` → `check-sprint-balance` + `check-sprint-dependencies`
   + `check-sprint-goal-coherence` + `score-sprint-plan-quality`.
4. `planner` → `decompose-task` + `estimate-effort` + `sequence-dependencies`
   — emits the canonical task plan with every coding step paired to a
   testing step.
5. For each step in the plan (orchestrator iterates):
   - `designer` → applicable design skills (UI steps only)
   - `frontend` or `backend` → tier-appropriate implementation skill
   - `tester` → matching testing skill + `run-tests`
   - `reviewer` → `code-review`
   - `security` → `security-scan` + `secret-scan` (any patch)
   - `accessibility-auditor` → all five WCAG checks (UI steps)
   - `performance-auditor` → bundle/render/network/CWV (UI or perf-sensitive)
6. `docs` → `update-readme` (if a documented surface changed) +
   `changelog-entry`.
7. `devops` → `build-artifact`.
8. `deployer` → `deploy-environment` (always human-gated for prod).

## Gating

- `infra-confidence` fires at every step. Floor 0.85; reviewers/auditors/deployer
  at 0.95.
- Sensitive surfaces (per `SPEC.md` §4) escalate to human regardless of confidence.
- Migrations are human-gated even when written by their owner agent.
