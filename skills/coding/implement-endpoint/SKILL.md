---
id: implement-endpoint
category: coding
owner_agent: coder
inputs:
  - route
  - method
  - request_schema
  - response_schema
outputs:
  - patch
requires_plan: true
emits_confidence: true
---

# Skill: implement-endpoint

## Task

Add one HTTP endpoint matching the schemas. Wire it into the router using
the framework's idiomatic mechanism. Validate the request, return the
response, and reject malformed input.

## Stop condition

Endpoint is reachable from the framework's test client and returns the
expected status codes for the schema cases.
