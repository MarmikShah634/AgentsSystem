---
id: infra-router
kind: infra
role: "Deterministic step dispatcher — ownership check + LLM adapter call"
owns:
  - skills/infra/route-step
hands_off_to:
  - infra-confidence
  - infra-logger
confidence_floor: 1.0
sensitive_surfaces: []
---

# Infra Router Agent

## Mission

Deterministic. Given one plan step, look up the owner agent in the
registry, refuse if mismatched, then call the LLM adapter (or the infra
agent itself, if the step targets infra). Returns the raw response;
confidence gating happens in `infra-confidence`, logging in `infra-logger`.

## Implementation

Python module: `orchestrator/infra/router.py`. Implements `handle(skill,
inputs)` for `route-step`.

## Why an agent?

So the orchestrator becomes a thin coordinator that invokes named
capabilities by id, not a god-object owning routing + gating + logging.
