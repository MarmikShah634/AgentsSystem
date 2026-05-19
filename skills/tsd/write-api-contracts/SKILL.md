---
id: write-api-contracts
category: tsd
owner_agent: tech-spec-author
inputs:
  - functional_requirements: "List of FRs with ids from the PRD; every user-facing capability that maps to an endpoint"
  - data_contracts: "JSON Schemas for every entity from write-data-contracts"
outputs:
  - section: "Markdown for the TSD API Contracts section; one block per endpoint"
  - confidence: "float in [0,1]"
requires_plan: true
emits_confidence: true
confidence_floor: 0.85
---

# Skill: write-api-contracts

## Purpose
Define every HTTP endpoint with its method, path, request and response JSON Schemas, auth requirements, rate-limit category, and worked examples. After this section, a backend agent can implement endpoints without inventing shapes, and a frontend agent can call them without reverse-engineering.

## When to invoke
Invoke after Data Contracts. Do NOT invoke to: implement an endpoint (use implement-endpoint), describe internal RPC between components (Component Contracts), or document third-party APIs (link to vendor docs in Overview).

## Procedure (follow exactly)
1. For each FR that implies an external call, emit a `### <METHOD> <path>` subsection.
2. Inside each subsection list:
   - **Auth**: `none` | `bearer` | `session` | named scopes; cite component that enforces it.
   - **Rate limit**: a category like `low`, `default`, `burst-tolerant`.
   - **Request**: JSON Schema for `path`, `query`, `body` (each as a separate sub-schema).
   - **Responses**: `200` (or `201`, `204`) JSON Schema referencing data contracts by `$ref` whenever possible, plus one entry for every non-2xx status from the error model.
   - **Examples**: at least one request/response pair per declared status code, fenced as ```json.
3. Reference data contracts via `$ref: "#/data-contracts/User"`; do not inline shapes that already exist as entities.
4. Reference error model codes by stable id (e.g. `AUTH_EXPIRED`) in each non-2xx response.
5. Do not invent endpoints not implied by an FR. Do not omit endpoints that an FR clearly requires.

## How to think
- One FR may map to several endpoints (CRUD). Make the mapping explicit per endpoint.
- Path conventions: nouns, plural, kebab/lowercase. No verbs in paths.
- If two endpoints differ only by query, keep them as one with query-driven behavior.
- If a response shape is new (not an entity), STOP and ask whether to extend data contracts.

## Required inputs
Both inputs must be non-empty. If `data_contracts` lacks an entity that an endpoint plainly needs, STOP — extend data contracts first.

## Output format
Markdown starting with `## API Contracts`. Each endpoint has `### METHOD /path`, then bolded sub-headings (Auth, Rate limit, Request, Responses, Examples), with fenced JSON Schemas.

## Quality criteria
Passes if: every FR with an external surface has at least one endpoint; every request field types to a data contract or primitive; every status code appears in the error model; every status has an example.
Fails if: endpoints invented without FR; status codes referenced but missing from error model; response shapes that don't $ref entities they should; examples missing.

## Common pitfalls
- Verbs in paths (`/getUser`).
- Returning a 200 with `{error: ...}` instead of a proper non-2xx.
- Duplicating entity fields inline rather than `$ref`.
- Forgetting the 4xx for validation failure.

## Examples
Good: `POST /v1/orders` with body `$ref Order`, response 201 `$ref Order`, 400 `VALIDATION_FAILED`, 401 `AUTH_EXPIRED`, with examples.
Bad: `POST /createOrder` returning 200 with a free-form error payload; no error codes referenced.

## Stop condition
Section exists, every FR with an external surface is covered, every endpoint has Auth/Rate/Request/Responses/Examples, every status code maps to an error model entry, and every reusable shape uses `$ref` to data contracts.

## Confidence guidance
Lower when: FR doesn't specify endpoint count (≤0.75), error model not yet written (≤0.7 — forward refs risky), data contracts incomplete (≤0.7), auth model unclear (≤0.75). Need ≥0.85.
