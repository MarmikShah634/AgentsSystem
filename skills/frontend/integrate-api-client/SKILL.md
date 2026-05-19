---
id: integrate-api-client
category: frontend
owner_agent: frontend
inputs:
  - endpoint: "HTTP method + path, e.g. GET /v1/users/{id}"
  - request_schema: "TypeScript type / Zod schema for path + query + body"
  - response_schema: "{status_code: type} per response"
  - error_model: "shape of 4xx/5xx error bodies the backend returns"
outputs:
  - patch: "unified diff of changes"
  - touched_paths: "list of files modified or created"
  - rationale: "1-3 sentences"
  - confidence: "float in [0,1]"
requires_plan: true
emits_confidence: true
confidence_floor: 0.85
---

# Skill: integrate-api-client

## Purpose
Add one strongly typed client function that calls one backend endpoint using the project's existing HTTP client. Map non-2xx responses to typed error classes per the project's error model.

## When to invoke
Invoke when the plan step is integrate an API client function AND the backend endpoint exists (or is in the same plan, declared) AND the project already has an HTTP client module. Reject if no HTTP client exists yet — that is a scaffold step.

## Procedure (follow exactly)
1. Locate the existing API client module (e.g. `src/api/client.ts`, `src/lib/http.ts`). Reuse it; do not create a parallel client.
2. Place the new function in the resource's existing file (e.g. `src/api/users.ts`). If none exists, create one matching the resource naming pattern.
3. Define request and response types from `request_schema` and `response_schema`. If the project uses Zod/Yup, define a schema and infer the type. Do not duplicate types — import shared types from `src/api/types.ts` if present.
4. Call the HTTP client with the typed payload. Pass path params through interpolation; query params through the client's params option; body as JSON.
5. Branch on status:
   - 2xx → parse and return the typed response.
   - 4xx/5xx → throw a typed error from the error model (`ApiError`, `NotFoundError`). Never throw raw strings.
6. Do not retry, do not cache — those are handled by the data layer.
7. Run the paired unit test that mocks the HTTP layer (`msw`, `nock`, `vi.mock`). Assert request shape, response shape, error mapping.

## How to think
- Endpoint not yet deployed → stub via the same typed contract; mark `confidence` lower and note in `rationale`.
- Backend returns inconsistent error shapes → STOP and ask human; do not paper over.
- Auth headers → reuse the client's existing interceptor; do not add ad-hoc headers.

## Required inputs
All four fields non-empty. `error_model` must enumerate the status codes the endpoint can return.

## Output format
{"patch": "unified diff", "touched_paths": ["src/api/users.ts", "src/api/users.test.ts"], "rationale": "1-3 sentences", "confidence": 0.0}

## Quality criteria
Passes if: types strict (no `any`); response narrowed by status; errors typed; mock test asserts request + response + at least one error; no new HTTP library.
Fails if: uses `fetch` directly when the project has a client; swallows errors; returns `unknown`; introduces retry/caching here.

## Common pitfalls
- `try/catch` that returns `null` on error. Throw a typed error instead.
- `JSON.parse(response.text)` when the client already parses. Trust the client.
- Building query strings by hand. Use the client's params option.

## Examples
TS with a shared client:
```ts
import { http } from './client';
import { UserSchema, type User } from './types';
import { ApiError, NotFoundError } from './errors';

export async function getUser(id: string): Promise<User> {
  const res = await http.get(`/v1/users/${id}`, { validateStatus: () => true });
  if (res.status === 200) return UserSchema.parse(res.data);
  if (res.status === 404) throw new NotFoundError('user', id);
  throw new ApiError(res.status, res.data);
}
```

Anti-pattern:
```ts
export async function getUser(id: string) {
  try { return (await fetch('/v1/users/' + id)).json(); }      // bypass client
  catch { return null; }                                        // swallow error
}
```

## Stop condition
Function compiles under strict TS; mock-based unit test passes for success and at least one error path; no new HTTP dep introduced.

## Confidence guidance
Lower when: error model unclear (≤0.7), backend endpoint not yet implemented (≤0.75), response schema ambiguous (≤0.75). Floor 0.85 to proceed.
