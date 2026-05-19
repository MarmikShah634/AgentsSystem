---
id: scaffold-project
category: coding
owner_agent: coder
inputs:
  - tech_stack
  - target_dir
outputs:
  - created_paths
requires_plan: true
emits_confidence: true
---

# Skill: scaffold-project

## Task

Create the minimal directory + config layout for the chosen tech stack.
Use the stack's native init tool (`npm init`, `cargo init`, `poetry new`,
`go mod init`, etc.) — do not hand-write boilerplate.

## Stop condition

Project runs an empty build/test successfully.
