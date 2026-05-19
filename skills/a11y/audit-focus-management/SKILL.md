---
id: audit-focus-management
category: a11y
owner_agent: accessibility-auditor
inputs:
  - target_path
outputs:
  - findings
requires_plan: true
emits_confidence: true
---

# Skill: audit-focus-management

## Task

WCAG 2.2 2.4.7/2.4.11. Verify:

- Visible focus indicator on every focusable element (≥2px outline).
- Focus moves to opened dialogs / drawers; returns on close.
- No focus trap outside modal contexts.
- `outline: none` is only allowed when paired with a custom focus style.
