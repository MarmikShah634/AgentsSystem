---
id: pick-color-palette-oklch
category: design
owner_agent: designer
inputs:
  - brand_context
  - colour_strategy
outputs:
  - palette
requires_plan: true
emits_confidence: true
---

# Skill: pick-color-palette-oklch

## Task

Emit one palette in OKLCH coordinates, given `brand_context` and one
`colour_strategy` on the Restrained → Drenched scale (impeccable).

## Rules (encoded from source skills)

1. Use OKLCH only. No hex/RGB/HSL in the palette output.
2. Never pure `#000000` or `#ffffff`. Always offset L by at least 5%.
3. **One** accent maximum. Saturation < 80% (taste-skill anti-AI-purple).
4. Provide 9 stops (50, 100, 200, … 900) per declared role
   (`bg`, `fg`, `accent`, `muted`, `border`).
5. State the chosen strategy explicitly in the output.

## Stop condition

Output is a JSON object `{strategy, roles: {bg: [...], fg: [...], ...}}`
where every value matches `oklch(L%  C  H)`.
