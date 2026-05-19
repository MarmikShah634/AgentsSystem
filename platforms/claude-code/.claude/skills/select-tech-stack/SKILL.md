---
id: select-tech-stack
category: design
owner_agent: architect
inputs:
  - requirements
  - detected_stack
outputs:
  - tech_stack
requires_plan: false
emits_confidence: true
---

# Skill: select-tech-stack

## Task

Pick (or confirm) language, framework, datastore, and key libraries.

## Procedure

1. If `detected_stack` is non-empty, default to it. Only deviate with
   a recorded justification per change.
2. Map each requirement to the stack components that satisfy it.
3. Output exactly one stack — no "options to consider".
