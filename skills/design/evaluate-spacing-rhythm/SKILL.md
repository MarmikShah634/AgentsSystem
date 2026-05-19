---
id: evaluate-spacing-rhythm
category: design
owner_agent: designer
inputs:
  - target_path
outputs:
  - findings
requires_plan: true
emits_confidence: true
---

# Skill: evaluate-spacing-rhythm

## Task

Flag UI regions that use uniform / default spacing. Enforce intentional
variance (impeccable principle: spacing rhythm is a design decision, not
a default).

## Checklist

1. Inspect padding/margin tokens across siblings.
2. Flag any group where every direct child uses the same vertical gap.
3. Flag any layout where vertical and horizontal gaps share one value.
4. Flag any "card grid" with identical card dimensions and gaps.

## Stop condition

Every flagged region has a concrete `fix` suggestion (e.g. "increase top
gap of `<section>` to 3× others to create a hero rhythm").
