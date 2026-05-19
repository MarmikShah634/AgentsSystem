---
id: tune-motion-physics
category: design
owner_agent: designer
inputs:
  - target_path
outputs:
  - findings
requires_plan: true
emits_confidence: true
---

# Skill: tune-motion-physics

## Task

Audit animations against the taste-skill motion budget.

## Checklist

1. Animate only `transform` and `opacity`. Flag any animation of `width`,
   `height`, `top`, `left`, `margin`, etc. (causes layout thrash).
2. Spring physics defaults: `stiffness: 100, damping: 20`. Flag custom
   values without justification.
3. Durations between 150ms and 400ms for UI transitions.
4. No infinite loops outside loading indicators.
5. Respect `prefers-reduced-motion` — every animation must have a
   reduced-motion fallback.

## Stop condition

Each violation includes a concrete `fix` (e.g. "replace `height: auto`
animation with `transform: scaleY` + `transform-origin: top`").
