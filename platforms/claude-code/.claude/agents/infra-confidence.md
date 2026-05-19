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

Deterministic. Given `confidence`, `touched_paths`, and the calling
`actor_agent`, decide whether to proceed or escalate to a human.

## Two gates

1. **Sensitive-surface gate** — paths matching the sensitive globs
   require human approval. Exception: a surface may have an
   *owner agent* (see `DEFAULT_OWNERSHIP` in the Python body); that owner
   can write without escalation. Any other actor still escalates.
2. **Confidence floor** — if `confidence < floor` (default 0.90) →
   escalate. Reviewers and auditors raise to 0.95. The owner bypass on
   the surface gate does NOT bypass this gate.

## Implementation

Python module: `orchestrator/infra/confidence.py`.
