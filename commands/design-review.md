---
id: design-review
description: "Run the designer agent over a UI surface and emit findings"
entry_agent: designer
---

# /design-review

**Usage:** `/design-review <path-or-route>`

Runs the full designer checklist:

1. `designer` → `evaluate-spacing-rhythm`
2. `designer` → `pick-color-palette-oklch` (if no palette declared yet)
3. `designer` → `audit-typography-scale`
4. `designer` → `detect-ai-slop-patterns`
5. `designer` → `tune-motion-physics`
6. `designer` → `enforce-interaction-states`
7. `designer` → `critique-ui-copy`

Emits a consolidated `findings[]` list. `frontend` agent applies the
fixes in a follow-up plan.
