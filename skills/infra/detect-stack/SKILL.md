---
id: detect-stack
category: infra
owner_agent: infra-stack-detector
inputs:
  - root
outputs:
  - stacks
requires_plan: false
emits_confidence: false
---

# Skill: detect-stack

Return the list of detected tech-stack signals at `root` (defaults to
cwd). See `orchestrator/infra/stack_detector.py:SIGNALS`.
