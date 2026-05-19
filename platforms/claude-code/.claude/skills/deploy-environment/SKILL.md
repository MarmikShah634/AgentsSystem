---
id: deploy-environment
category: deploy
owner_agent: deployer
inputs:
  - artifact_path
  - environment
outputs:
  - release_id
requires_plan: true
emits_confidence: true
---

# Skill: deploy-environment

## Task

Promote the artifact to `environment`. Production is always human-gated.
Emit the new `release_id` and a `rollback_ref` to the previous release.
