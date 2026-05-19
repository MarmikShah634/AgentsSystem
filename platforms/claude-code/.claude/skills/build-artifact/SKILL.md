---
id: build-artifact
category: deploy
owner_agent: devops
inputs:
  - target
outputs:
  - artifact_path
requires_plan: true
emits_confidence: true
---

# Skill: build-artifact

## Task

Run the stack's native build command. Emit the artifact path.
