---
id: score-sprint-plan-quality
category: sprint
owner_agent: sprint-reviewer
inputs:
  - findings: "aggregated array from check-sprint-balance, check-sprint-dependencies, check-sprint-goal-coherence"
outputs:
  - readiness_score: "float in [0,1]"
  - verdict: "'pass' | 'revise'"
  - rationale: "1-3 sentences naming the largest deductions"
  - confidence: "float in [0,1]"
requires_plan: true
emits_confidence: true
confidence_floor: 0.95
---

# Skill: score-sprint-plan-quality

## Purpose
Aggregate sprint-reviewer findings into a single readiness score and pass/revise verdict. Deterministic formula; no narrative judgement.

## When to invoke
Invoke when findings from all three sprint-reviewer check skills are present (balance, dependencies, goal-coherence).
Do NOT invoke to: produce findings (use the dedicated check-* skills), rewrite the plan, or score non-sprint artifacts.

## Procedure (follow exactly)
1. Initialize `score = 1.0`.
2. Apply the deduction table:
   - −0.20 per cyclic dependency finding (severity=error from check-sprint-dependencies, "cycle" in msg).
   - −0.15 per over-committed sprint (severity=error from check-sprint-balance).
   - −0.10 per incoherent goal (severity=error from check-sprint-goal-coherence).
   - −0.05 per warn finding from any source.
3. Clamp `score` to [0, 1].
4. Set `verdict = "pass"` if `score >= 0.85`, else `"revise"`.
5. Write rationale citing the top two deductions by magnitude (e.g., "−0.30 from 2 cycles; −0.15 from SP2 over-commit").
6. Emit `readiness_score`, `verdict`, `rationale`, and `confidence`.

## How to think
- Same finding appears in two sources → count once.
- Warn finding contains no severity field → treat as warn (−0.05).
- Score is exactly 0.85 → pass (boundary inclusive).
- No findings → score 1.0, verdict pass; rationale "no deductions".

## Required inputs
`findings` array (possibly empty). Each finding must include `severity` and `msg`. Missing fields → STOP.

## Output format
```json
{"readiness_score":0.65,"verdict":"revise",
 "rationale":"−0.20 cycle in S2↔S5; −0.15 SP2 over-commit at 28/25.",
 "confidence":0.0}
```

## Quality criteria
Passes if: deductions match the table exactly; score clamped to [0,1]; verdict respects 0.85 threshold; rationale names two largest deductions.
Fails if: arithmetic error; verdict mis-flipped at boundary; rationale generic; deductions double-counted across sources.

## Common pitfalls
- Treating warn as error.
- Counting the same cycle twice when it appears in multiple findings.
- Reporting unrounded floats; round to 2 decimals.
- Issuing a verdict without applying the deduction table.

## Examples
✅ Findings: 1 cycle, 1 over-commit, 1 warn. Score = 1.0 − 0.20 − 0.15 − 0.05 = 0.60 → revise. Rationale names the cycle and the over-commit.
❌ Anti-pattern: emitting "looks risky" verdict without applying the formula.

## Stop condition
Score computed via the deduction table, verdict assigned at the 0.85 threshold, rationale names the largest deductions.

## Confidence guidance
This skill is deterministic — confidence should usually be 1.0. Lower only when findings are malformed (≤0.95). Floor 0.95 enforced.
