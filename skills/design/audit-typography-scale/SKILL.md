---
id: audit-typography-scale
category: design
owner_agent: designer
inputs:
  - target_path
outputs:
  - findings
requires_plan: true
emits_confidence: true
---

# Skill: audit-typography-scale

## Task

Audit type for measure, scale ratio, and font choice.

## Checklist

1. Body copy measure between 65–75ch. Flag any block outside.
2. Type scale ratio ≥ 1.25 (perfect fourth or larger). Flag flat scales.
3. Banned families: Inter. Prefer Geist / Outfit / Cabinet Grotesk /
   Satoshi (taste-skill).
4. At most 2 families total (one display, one body).
5. Line-height ≥ 1.5 for body, ≤ 1.2 for display.

## Stop condition

Findings list every violation with `path`, `line`, and a `fix` field.
