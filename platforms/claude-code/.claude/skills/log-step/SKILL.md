---
id: log-step
category: infra
owner_agent: infra-logger
inputs:
  - record
outputs:
  - written_path
requires_plan: false
emits_confidence: false
---

# Skill: log-step

Append one record to `logs/audit/<date>.jsonl`. Hashes `inputs` and
`outputs` to SHA-256 before writing.
