---
id: check-sprint-dependencies
category: sprint
owner_agent: sprint-reviewer
inputs:
  - sprints: "array of {sprint_id, story_ids, stories: [{story_id, depends_on}]}"
outputs:
  - findings: "array of {area, severity, sprint_id, story_id, msg, fix}"
  - confidence: "float in [0,1]"
requires_plan: true
emits_confidence: true
confidence_floor: 0.85
---

# Skill: check-sprint-dependencies

## Purpose
Detect dependency violations across sprints: cycles, backward dependencies (story depends on a later sprint), and overlong chains that signal incorrect slicing.

## When to invoke
Invoke when every story carries `depends_on` AND every story is placed in exactly one sprint.
Do NOT invoke to: check balance (use check-sprint-balance), check goal coherence (use check-sprint-goal-coherence), or rewrite the sprint plan.

## Procedure (follow exactly)
1. Build a story-level DAG from `depends_on`.
2. Detect cycles via Kahn's algorithm. Any cycle → emit `severity: "error"` listing the cycle.
3. For each dependency edge A→B, locate the sprint indices of A and B. If sprint_index(A) > sprint_index(B), emit `severity: "error"`: B requires a predecessor scheduled later.
4. If sprint_index(B) - sprint_index(A) > 2 (predecessor more than two sprints earlier than dependent), emit `severity: "warn"` for suspected over-slicing.
5. Every finding includes `fix` naming the specific story to move and where.
6. Emit findings; do not rewrite the plan.

## How to think
- Edge within the same sprint → fine; ordering inside a sprint is the team's call.
- Predecessor exactly two sprints earlier → at the boundary; pass.
- Cycle includes ≥3 stories → still one finding; list the full cycle.
- Predecessor in same sprint as dependent but unscheduled before it → not this skill's concern.

## Required inputs
Story-level `depends_on`; sprint placements. Missing edges or unhydrated stories → STOP.

## Output format
```json
{"findings":[
  {"area":"dependencies","severity":"error","sprint_id":"SP1","story_id":"S2",
   "msg":"S2 depends on S5 which is in SP3.",
   "fix":"move S2 to SP3 or pull S5 forward to SP1."}],
 "confidence":0.0}
```

## Quality criteria
Passes if: cycles flagged as errors; backward deps flagged as errors; >2-sprint gaps flagged as warns; every finding has a concrete fix naming stories and sprints.
Fails if: cycle silently dropped; backward dep classified as warn; fix omits specific story_ids; plan rewritten instead of flagged.

## Common pitfalls
- Treating same-sprint dependencies as findings.
- Confusing story_id strings with sprint_ids in messages.
- Missing the cycle when it spans >2 stories.
- Issuing fixes like "review dependencies" without naming stories.

## Examples
✅ Finding: severity=error, story=S2 in SP1, msg="S2 depends on S5 in SP3", fix="move S2 to SP3".
❌ Anti-pattern: emitting "dependency issues found" with no story/sprint names.

## Stop condition
Every dependency edge checked; cycles, backward deps, and overlong chains each emitted with concrete fixes.

## Confidence guidance
Lower when: dependency graph sparse/incomplete (≤0.75), implicit dependencies suspected but not modeled (≤0.7), >50 stories (≤0.8). ≥0.85 required.
