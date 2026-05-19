---
id: generate-architecture-diagram
category: architecture
owner_agent: architect
inputs:
  - components
outputs:
  - mermaid_diagram
requires_plan: false
emits_confidence: true
---

# Skill: generate-architecture-diagram

## Task

Emit a Mermaid `flowchart` describing components and their dependencies.
No prose, just the Mermaid block.
