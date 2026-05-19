---
id: refactor-frontend
category: frontend
owner_agent: frontend
inputs:
  - target_paths
  - refactor_goal
outputs:
  - patch
requires_plan: true
emits_confidence: true
---

# Skill: refactor-frontend

## Task

Behaviour-preserving change limited to UI-tier paths. Visual output must
be identical (Puppeteer screenshot diff <1%).

## Do NOT

- Change public component APIs.
- Touch server-side files.
- Add libraries.
