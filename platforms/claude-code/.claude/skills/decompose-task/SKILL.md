---
id: decompose-task
category: planning
owner_agent: planner
inputs:
  - requirements: "validated PRD/TSD or sprint payload defining the goal in concrete acceptance criteria"
  - architecture: "TSD architecture section: components, contracts, data flow, sensitive surfaces"
outputs:
  - plan_steps: "ordered list of {step_id, agent, skill, category, inputs, expected_outputs, depends_on, test_pair, human_gate}"
  - rationale: "1-3 sentences explaining the decomposition strategy"
  - confidence: "float in [0,1]"
requires_plan: false
emits_confidence: true
confidence_floor: 0.85
---

# Skill: decompose-task

## Purpose
Convert one validated sprint (or feature goal) into an ordered DAG of plan steps where each step is exactly one skill invocation by one agent. The output is the contract the orchestrator executes; ambiguity here propagates everywhere downstream.

## When to invoke
Invoke when the requirements input is non-empty AND the architecture input names every component the goal touches AND no prior plan_steps array exists for this goal.
Do NOT invoke to: re-plan after a failed step (use replan-from-failure), expand a single step (use the relevant decompose-* skill), or break down PRD epics (use group-prd-into-epics).

## Procedure (follow exactly)
1. Read every acceptance criterion in `requirements`. List them as ACs.
2. For each AC, identify the touched components from `architecture`.
3. For each touched component, allocate one coding step (frontend, backend, or infra) and immediately allocate its paired testing step.
4. Assign exactly one `skill` and one `agent` per step. Never combine skills.
5. Wire `depends_on` so that schema/contract steps precede consumers; coding precedes its own test; integration tests depend on all coding steps in their scope.
6. Mark `human_gate: true` for any step touching a sensitive surface listed in SPEC.md §4 (auth, billing, secrets, prod deploy, schema migrations on prod data).
7. Topologically order the array; verify no cycles before emitting.

## How to think
- Step spans more than one skill → split it.
- Step has no test pair → add one before emitting.
- AC implies a new architectural component not in `architecture` → STOP and lower confidence; do not invent components.
- Two steps appear identical except for path → they are still two steps; do not collapse.

## Required inputs
`requirements` must include ACs; `architecture` must enumerate components. If either is missing or vague, STOP and ask human — do not infer.

## Output format
```json
{
  "plan_steps": [
    {"step_id":"s1","agent":"backend","skill":"implement-endpoint","category":"coding",
     "inputs":{...},"expected_outputs":["patch"],"depends_on":[],"test_pair":"s2","human_gate":false}
  ],
  "rationale":"...",
  "confidence":0.0
}
```

## Quality criteria
Passes if: every coding step has a `test_pair`; every `depends_on` references an earlier `step_id`; every sensitive-surface step has `human_gate: true`; no step references two skills; every AC maps to ≥1 step.
Fails if: any cycle; any orphan step (no AC covered); any step missing `agent` or `skill`; any sensitive-surface step without `human_gate`.

## Common pitfalls
- Folding "implement + test" into one step.
- Omitting `depends_on` for steps that read another step's artifact.
- Skipping the `human_gate` flag on auth/payment/migration work.
- Inventing component names absent from `architecture`.
- Producing parallel steps that secretly write the same file (use sequencing).

## Examples
✅ Goal "add /v1/sessions endpoint": s1=design-schema → s2=implement-endpoint (test_pair=s3) → s3=write-integration-test → s4=document-endpoint. depends_on chain is linear.
❌ Anti-pattern: one step "build sessions feature" with skill `implement-feature`, no test pair, no schema step, no human_gate even though sessions writes auth tokens.

## Stop condition
Every AC is covered by ≥1 step; every coding step has a test_pair; DAG is acyclic; output validates against the schema above.

## Confidence guidance
Lower when: ACs ambiguous (≤0.7), architecture incomplete (≤0.65), sensitive surface unclear (≤0.7), >15 steps required (≤0.8). ≥0.85 required to emit without human gate.
