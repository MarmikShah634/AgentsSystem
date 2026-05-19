---
id: rollback
category: deploy
owner_agent: deployer
inputs:
  - environment
  - rollback_ref
outputs:
  - restored_release_id
requires_plan: true
emits_confidence: true
---

# Skill: rollback

## Task

Roll back `environment` to `rollback_ref`. ALWAYS human-gated. Emit the
restored release id.
