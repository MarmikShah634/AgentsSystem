---
id: audit-color-contrast
category: a11y
owner_agent: accessibility-auditor
inputs:
  - target_path
outputs:
  - findings
requires_plan: true
emits_confidence: true
---

# Skill: audit-color-contrast

## Task

WCAG 2.2 1.4.3/1.4.11. For every text-on-background pair:

- Body text: contrast ≥ 4.5:1.
- Large text (≥18pt or 14pt bold): ≥ 3:1.
- UI components & graphical objects: ≥ 3:1.

Use the project's tokens; flag any failing pair with `wcag: "1.4.3"` and
both colours + measured ratio.
