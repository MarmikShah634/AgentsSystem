---
id: audit-screen-reader-flow
category: a11y
owner_agent: accessibility-auditor
inputs:
  - target_path
outputs:
  - findings
requires_plan: true
emits_confidence: true
---

# Skill: audit-screen-reader-flow

## Task

WCAG 2.2 1.3.1/4.1.3. Validate semantic structure:

- One `<h1>` per page; heading hierarchy unbroken.
- Landmarks present: `<main>`, `<nav>`, `<header>`, `<footer>`.
- Dynamic regions use `aria-live`.
- Decorative elements set `aria-hidden="true"`.
