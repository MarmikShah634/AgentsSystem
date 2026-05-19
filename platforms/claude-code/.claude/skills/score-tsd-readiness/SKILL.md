---
id: score-tsd-readiness
category: tsd
owner_agent: tech-spec-reviewer
inputs:
  - findings: "Combined list of finding objects from check-tsd-completeness, check-tsd-implementability, check-tsd-contract-consistency"
outputs:
  - readiness_score: "Float in [0.0, 1.0] computed from finding kinds"
  - verdict: "'pass' if readiness_score >= 0.90 else 'revise'"
  - confidence: "float in [0,1]"
requires_plan: true
emits_confidence: true
confidence_floor: 0.95
---

# Skill: score-tsd-readiness

## Purpose
Aggregate all reviewer findings into a single readiness score and a pass/revise verdict. The score gates whether the TSD proceeds to implementation; the verdict is the contract the orchestrator reads.

## When to invoke
Invoke after all three reviewer skills have run and their findings are merged. Do NOT invoke to: re-check the TSD, rewrite findings, or produce qualitative narratives.

## Procedure (follow exactly)
1. Parse `findings`. Each finding must have a `kind` in {`incomplete`, `inconsistent`, `unimplementable`}; ignore any others and report parse errors.
2. Compute:
   ```
   score = 1.0
     - 0.25 per finding where kind == "incomplete"
     - 0.20 per finding where kind == "inconsistent"
     - 0.15 per finding where kind == "unimplementable"
   floor score at 0.0
   ```
3. Set `verdict = "pass"` iff `score >= 0.90`, else `"revise"`.
4. Round score to 2 decimals.
5. Return the score, verdict, and your confidence in the aggregation.

## How to think
- This is a deterministic aggregator. Do not adjust the formula for taste.
- Confidence is about parsing accuracy, not about the TSD quality.
- If many findings cluster around one cause, that does not change the math.
- Verdict thresholds are hard cutoffs; 0.899 is `revise`.

## Required inputs
`findings` must be a list (possibly empty). Each item must be a dict with at least `kind`. Empty list yields `score=1.0`, `verdict="pass"`.

## Output format
```
{"readiness_score": 0.85, "verdict": "revise", "confidence": 0.98}
```

## Quality criteria
Passes if: arithmetic exact per the formula; verdict matches threshold; rounding to 2 decimals; floor at 0.0 applied.
Fails if: weights tweaked; verdict threshold deviates from 0.90; unrecognized kinds silently ignored without reporting.

## Common pitfalls
- "Adjusting" the score because the findings feel minor.
- Forgetting to floor at 0.0 when many findings push it negative.
- Confusing the input's per-finding `confidence` with this skill's aggregation confidence.
- Reporting verdict `pass` at 0.89.

## Examples
Good: 1 incomplete + 1 inconsistent → score `1.0 - 0.25 - 0.20 = 0.55`, verdict `revise`.
Bad: 1 incomplete → rounding up to `0.80`, calling it `pass`.

## Stop condition
A single object is produced with `readiness_score` (2-decimal float), `verdict` (`pass` or `revise`), and `confidence`. The TSD was not modified. No findings were dropped without a parse-error report.

## Confidence guidance
Lower when: findings contain unrecognized kinds (≤0.95), findings duplicate the same issue (≤0.95 — caller may want dedup), input list size very large (>50) raising parse risk (≤0.95). Required floor 0.95.
