---
id: integrate-api-client
category: frontend
owner_agent: frontend
inputs:
  - endpoint
  - request_schema
  - response_schema
outputs:
  - patch
requires_plan: true
emits_confidence: true
---

# Skill: integrate-api-client

## Task

Add one typed client function calling one backend endpoint. Use the
project's existing HTTP client. Handle non-2xx as typed errors.

## Stop condition

Client function compiles with strict types; paired unit test mocks the
endpoint and asserts request/response shapes.
