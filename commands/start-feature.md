---
id: start-feature
description: "Kick off a new feature from a human-supplied goal"
entry_agent: requirements
---

# /start-feature

**Usage:** `/start-feature <goal>`

Runs the full lifecycle:

1. `requirements` → `gather-user-stories`
2. `requirements` → `extract-acceptance-criteria`
3. `requirements` → `validate-requirements`
4. `architect` → `select-tech-stack`
5. `architect` → `generate-architecture-diagram`
6. `architect` → `design-data-model`
7. `planner` → `decompose-task` (+ `sequence-dependencies`)
8. For each step in the plan:
   - `coder` → coding skill
   - `tester` → matching testing skill
   - `tester` → `run-tests`
   - `reviewer` → `code-review`
   - `security` → `security-scan` + `secret-scan`
9. `docs` → `update-readme` + `changelog-entry`
10. `devops` → `build-artifact`
11. `deployer` → `deploy-environment` (human-gated)

Confidence gate fires at every step.
