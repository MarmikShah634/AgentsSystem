---
id: write-data-contracts
category: tsd
owner_agent: tech-spec-author
inputs:
  - data_model
outputs:
  - section
requires_plan: true
emits_confidence: true
---

# Skill: write-data-contracts

## Task

For each entity:

- Field list with types + nullability + units.
- Primary key + uniqueness constraints.
- Validation rules (regex, range, enum).
- Lifecycle (created_at, updated_at, soft-delete?).

JSON Schema or equivalent; no ORM-specific syntax.

## Stop condition

Every entity has all four fields; no `string` field is left without a
length bound.
