---
id: infra-confidence
kind: infra
role: "Confidence gate evaluator — floor + sensitive surfaces"
owns:
  - skills/infra/evaluate-confidence
hands_off_to: []
confidence_floor: 1.0
sensitive_surfaces: []
---

# Infra Confidence Agent

## Mission

Deterministic. Given `confidence` and `touched_paths`, decide whether to
proceed or escalate to a human. Encodes the 0.90 floor and the
sensitive-surface globs.

## Implementation

Python module: `orchestrator/infra/confidence.py`.
