---
id: group-prd-into-epics
category: sprint
owner_agent: sprint-planner
inputs:
  - prd_path: "absolute path to a validated PRD with numbered Functional Requirements (FRs)"
outputs:
  - epics: "array of {epic_id, name, persona_or_workflow, fr_ids, rationale}"
  - rationale: "1-3 sentences on clustering strategy"
  - confidence: "float in [0,1]"
requires_plan: true
emits_confidence: true
confidence_floor: 0.85
---

# Skill: group-prd-into-epics

## Purpose
Cluster every PRD Functional Requirement into 3-8 epics. Each epic is a shippable narrative scoped to one persona or one workflow, providing the next layer for story decomposition.

## When to invoke
Invoke when the PRD at `prd_path` is validated AND its FRs are numbered AND no prior epic list exists.
Do NOT invoke to: refine an existing epic (use decompose-epic-into-stories), group non-PRD inputs, or produce a backlog of tasks.

## Procedure (follow exactly)
1. Read every FR. List FR id, title, and stated persona/workflow.
2. Cluster FRs by shared persona OR shared workflow (not by component/layer).
3. Aim for 3-8 epics. If the count would fall outside that range, re-cluster — never emit <3 or >8.
4. Name each epic in noun form ("Auth", "Checkout", "Onboarding"). Reject verb names ("Build login", "Add cart").
5. Verify every FR appears in exactly one epic. No duplicates, no orphans.
6. Write a one-line rationale per epic citing the persona or workflow.

## How to think
- FR fits two epics → pick the one whose persona owns the primary user goal; cite in rationale.
- Epic count > 8 → cluster sub-epics under a parent persona.
- Epic count < 3 → split the largest epic by workflow stage.
- FR is cross-cutting (logging, observability) → it belongs to a "Platform" epic, not duplicated.

## Required inputs
`prd_path` must resolve to a file with numbered FRs. Unnumbered or empty PRD → STOP and ask human.

## Output format
```json
{"epics":[
  {"epic_id":"E1","name":"Auth","persona_or_workflow":"new user",
   "fr_ids":["FR-3","FR-4","FR-7"],"rationale":"covers signup+login flow"}],
 "rationale":"clustered by persona; 5 epics total.",
 "confidence":0.0}
```

## Quality criteria
Passes if: 3-8 epics; every FR mapped exactly once; every epic name is a noun; every epic cites persona or workflow.
Fails if: any FR missing or duplicated; verb-named epic; epic without persona/workflow tag; count outside 3-8.

## Common pitfalls
- Clustering by technology layer ("Frontend", "Backend") — forbidden.
- Verb-form epic names like "Implement payments".
- Allowing one FR to live in two epics for convenience.
- Forgetting Platform/observability FRs and producing orphans.

## Examples
✅ Epics: Auth, Checkout, Catalog, Platform. FR-1..FR-20 mapped one-to-one. Rationale: clustered by user-facing workflow.
❌ Anti-pattern: 12 epics named "Login API", "Login UI", "Login DB" — splits by layer not persona; over the cap.

## Stop condition
Every FR mapped exactly once, 3-8 noun-named epics emitted, each tagged with persona or workflow.

## Confidence guidance
Lower when: PRD FRs ambiguous (≤0.7), persona unstated (≤0.75), >25 FRs (≤0.8). ≥0.85 required.
