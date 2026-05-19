---
id: plan
description: "Generate a plan for a goal without executing it"
entry_agent: planner
---

# /plan

**Usage:** `/plan <goal>`

Runs requirements + architect + planner stages only, writes the plan to
`logs/plans/<uuid>.json`, and prints the plan id. Nothing else runs.
