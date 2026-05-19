---
id: configure-ci
category: deploy
owner_agent: devops
inputs:
  - ci_system
  - jobs
outputs:
  - ci_config_path
requires_plan: true
emits_confidence: true
---

# Skill: configure-ci

## Task

Author / update the CI pipeline definition for the detected CI system.
Each job is one of: install, lint, test, build, deploy. This skill is
human-gated by default.
