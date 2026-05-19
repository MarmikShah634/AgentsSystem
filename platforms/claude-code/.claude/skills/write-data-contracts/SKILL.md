---
id: write-data-contracts
category: tsd
owner_agent: tech-spec-author
inputs:
  - data_model: "Mermaid erDiagram + notes from design-data-model, listing entities/attributes/relationships"
outputs:
  - section: "Markdown for the TSD Data Contracts section; one JSON Schema per entity"
  - confidence: "float in [0,1]"
requires_plan: true
emits_confidence: true
confidence_floor: 0.85
---

# Skill: write-data-contracts

## Purpose
Translate each entity from the ER diagram into a precise JSON Schema (or equivalent) covering types, nullability, units, primary keys, uniqueness, validation rules, and lifecycle fields. Downstream API contracts will reference these by entity name; ambiguity here propagates into every endpoint.

## When to invoke
Invoke after Component Contracts and before API Contracts. Do NOT invoke to: write migrations (a backend skill), define DTOs that diverge from entities (use API Contracts), or pick a specific datastore syntax.

## Procedure (follow exactly)
1. For each entity in `data_model`, emit a `### <Entity>` subsection with a JSON Schema fenced as ```json.
2. Fields must include: `type`, `nullable` (explicit true/false), `unit` when numeric (e.g. `"unit": "ms"`), and `description`.
3. Mark the primary key under `x-primary-key`. Mark uniqueness constraints under `x-unique` as an array of field-name arrays.
4. Add validation: `pattern` for strings, `minimum`/`maximum` for numbers, `enum` for closed sets, `maxLength` for every string field (no unbounded strings).
5. Add lifecycle fields `created_at` (datetime, not null), `updated_at` (datetime, not null), and `deleted_at` (datetime, nullable) only if soft-delete is required by a requirement.
6. Do NOT use ORM types (`varchar`, `BIGINT`). Do NOT reference physical indices.

## How to think
- Every string needs a length bound; unbounded strings are a security hole.
- `nullable` must be explicit; default-undefined is ambiguous.
- If validation rules conflict with the ER diagram, the ER diagram wins for shape, this skill wins for constraints.
- If a field's unit is ambiguous (cents vs dollars), STOP and ask.

## Required inputs
`data_model` must contain at least one entity with attributes. If the diagram has entities with no attributes, STOP.

## Output format
Markdown starting with `## Data Contracts`. Each entity gets a `### <Entity>` with a fenced JSON Schema block including `properties`, `required`, `x-primary-key`, optional `x-unique`.

## Quality criteria
Passes if: every entity rendered; every string has `maxLength`; every nullable explicit; PK marked; lifecycle fields consistent; enums fully enumerated.
Fails if: unbounded strings; ORM types; PK missing; nullable unspecified; ambiguous units.

## Common pitfalls
- `"type": "string"` with no `maxLength`.
- Mixing units (seconds vs milliseconds) across fields without declaring `unit`.
- Adding indices or storage hints (out of scope).
- Diverging field names from the ER diagram.

## Examples
Good: `{"email": {"type": "string", "maxLength": 320, "pattern": "^[^@]+@[^@]+$", "nullable": false}}` with `x-primary-key: id` and `x-unique: [["email"]]`.
Bad: `{"email": "varchar"}`, no length, no nullability, no PK.

## Stop condition
Section exists with one JSON Schema per entity, every field typed and bounded, every PK and uniqueness constraint declared, lifecycle handled consistently, and zero ORM-specific syntax.

## Confidence guidance
Lower when: ER diagram lacks attributes (≤0.7), units ambiguous (≤0.7), enums infer from PRD prose (≤0.75), soft-delete need unclear (≤0.8). Need ≥0.85.
