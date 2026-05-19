---
id: ship-it
description: "Run build → security → deploy, human-gated for prod"
entry_agent: devops
---

# /ship-it

**Usage:** `/ship-it <environment>`

1. `devops` → `build-artifact`
2. `security` → `dependency-audit`
3. `pre-deploy-check.sh` hook
4. `deployer` → `deploy-environment` (prod always human-gated)
