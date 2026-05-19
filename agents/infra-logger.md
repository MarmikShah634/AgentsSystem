---
id: infra-logger
kind: infra
role: "Append-only audit log + plan persistence"
owns:
  - skills/infra/log-step
  - skills/infra/save-plan
  - skills/infra/load-plan
hands_off_to: []
confidence_floor: 1.0
sensitive_surfaces: []
---

# Infra Logger Agent

## Mission

Deterministic. Writes audit records to `logs/audit/<date>.jsonl` and
plans to `logs/plans/<uuid>.json`. Hash-stamps inputs/outputs.

## Implementation

Python module: `orchestrator/infra/logger.py`.
