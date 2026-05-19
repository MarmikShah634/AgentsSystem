---
id: implement-data-model
category: backend
owner_agent: backend
inputs:
  - model_name
  - fields_schema
outputs:
  - patch
requires_plan: true
emits_confidence: true
---

# Skill: implement-data-model

## Task

Define one persistence model (ORM entity, schema, struct). No queries,
no migrations — those are separate skills.

## Stop condition

Model loads with the ORM/driver and validates against its declared
schema in the paired unit test.
