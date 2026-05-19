---
id: estimate-effort
category: planning
owner_agent: planner
inputs:
  - plan_steps: "ordered DAG of plan steps from decompose-task"
outputs:
  - effort_estimate: "{per_step: {step_id: size}, total: size} where size in {XS,S,M,L,XL}"
  - rationale: "1-3 sentences explaining outliers and aggregation rule"
  - confidence: "float in [0,1]"
requires_plan: false
emits_confidence: true
confidence_floor: 0.85
---

# Skill: estimate-effort

## Purpose
Assign a calibrated t-shirt size to each plan step and a single rolled-up total. The estimate gates whether a sprint can absorb the plan and signals where to split work that is too coarse.

## When to invoke
Invoke when `plan_steps` is non-empty AND every step has a `skill` and `agent` assigned. Run once per plan, after `decompose-task` and before `sequence-dependencies`.
Do NOT invoke to: estimate stories in points (use estimate-story-points), produce wall-clock time, or commit to deadlines.

## Procedure (follow exactly)
1. For each step, classify by skill type: pure config (XS), single file edit (S), single component with paired test (M), cross-cutting refactor (L), multi-surface or migration (XL).
2. Adjust up one size if `human_gate: true` (review overhead).
3. Adjust up one size if `depends_on` length ≥ 3 (integration overhead).
4. Cap any single step at XL; if a step naturally exceeds XL, STOP and require the caller to re-decompose.
5. Compute `total` using the rollup table below (not arithmetic mean).
6. Emit per-step and total; include rationale citing outliers.

## How to think
- Step touches only YAML/JSON config → XS regardless of file count under 3.
- Step changes a schema consumed by ≥2 other steps → at least M, often L.
- Step is "wire-up only" but spans 3+ files → S becomes M.
- Estimate feels like a coin flip between two sizes → pick the larger and note in rationale.

## Required inputs
`plan_steps` must contain `skill`, `agent`, and `depends_on`. Missing fields → STOP and ask for completed decomposition.

## Output format
```json
{"effort_estimate":{"per_step":{"s1":"S","s2":"M"},"total":"L"},
 "rationale":"...","confidence":0.0}
```

Rollup table:
- ≤3 S-or-smaller → S
- mix of S/M with no L → M
- ≥1 L → L
- ≥1 XL or ≥3 L → XL

## Quality criteria
Passes if: every `step_id` in `plan_steps` has an entry; no step exceeds XL; rollup matches the table; rationale names the largest 1-2 steps.
Fails if: missing step; arithmetic-mean rollup; XL step not flagged for re-decomposition; rationale absent or generic.

## Common pitfalls
- Averaging sizes numerically (S=1, M=2…) instead of using the rollup table.
- Treating test pairs as "free" — they are at least S each.
- Ignoring human-gate overhead.
- Calling a migration step M because the diff is small.

## Examples
✅ 4 steps: s1=XS (config), s2=M (endpoint), s3=S (test), s4=M (frontend wire). Total=M. Rationale notes endpoint and frontend are the long poles.
❌ Anti-pattern: averaging to "S" when one step is XL, hiding the risk.

## Stop condition
Every step sized; total derived from the rollup table; no step at XL without an attached re-decomposition warning.

## Confidence guidance
Lower when: unfamiliar skill (≤0.75), step crosses ≥3 components (≤0.7), data missing on `depends_on` (≤0.7). ≥0.85 required.
