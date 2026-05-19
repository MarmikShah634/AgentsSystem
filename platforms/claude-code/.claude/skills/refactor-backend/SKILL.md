---
id: refactor-backend
category: backend
owner_agent: backend
inputs:
  - target_paths
  - refactor_goal
outputs:
  - patch
requires_plan: true
emits_confidence: true
---

# Skill: refactor-backend

## Task

Behaviour-preserving change limited to server-tier paths. Public API
surface (HTTP routes + request/response schemas) must not change.

## Do NOT

- Change endpoint URLs, methods, or schemas.
- Touch UI-tier files.
- Add libraries.
