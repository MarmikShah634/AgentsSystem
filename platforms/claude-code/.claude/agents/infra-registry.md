---
id: infra-registry
kind: infra
role: "Agent + skill lookup"
owns:
  - skills/infra/lookup-owner
  - skills/infra/list-agents
  - skills/infra/list-skills
hands_off_to: []
confidence_floor: 1.0
sensitive_surfaces: []
---

# Infra Registry Agent

## Mission

Deterministic. Loads `agents/*.md` and `skills/**/SKILL.md` and exposes
lookups: skill → owner agent, agent list, skill list.

## Implementation

Python module: `orchestrator/infra/registry.py`.
