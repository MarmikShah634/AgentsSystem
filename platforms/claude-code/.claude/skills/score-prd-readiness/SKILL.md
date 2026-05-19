---
id: score-prd-readiness
category: prd
owner_agent: prd-reviewer
inputs:
  - findings: "aggregated list of {section, kind, ...} from the five PRD check-* skills"
outputs:
  - readiness_score: "float in [0,1] — overall PRD readiness"
  - verdict: "'pass' if score >= 0.85 else 'revise'"
  - trace: "string showing the formula breakdown"
  - confidence: "float in [0,1]"
requires_plan: true
emits_confidence: true
confidence_floor: 0.95
---

# Skill: score-prd-readiness

## Purpose
Aggregate findings from all PRD check skills into one 0.0-1.0 readiness score and a `pass|revise` verdict. The score determines whether the PRD proceeds to the architect or returns to the prd-author. Deterministic formula; no judgement.

## When to invoke
Invoke as the FINAL prd-reviewer skill, after all five check-prd-* skills have run and their findings are collected. Run exactly once per review pass.

Do NOT invoke to: emit individual findings (each check-prd-* skill does that), gate the architect hand-off (the orchestrator does that based on this verdict), or rewrite the PRD.

## Procedure (follow exactly)
1. Receive the aggregated `findings` array. Count occurrences by kind:
   - n_missing      — `kind` in {missing, empty, skeleton} from check-prd-completeness
   - n_conflicting  — `kind == "conflicting"` from check-prd-conflicts
   - n_untestable   — `kind == "untestable"` from check-prd-testability
   - n_metric       — `kind` in {missing-field, vanity, unmapped, direction-mismatch, unmeasurable} from check-prd-metrics-quality
   - n_ambiguous    — `kind == "ambiguous"` from check-prd-ambiguity
2. Apply the scoring formula:
   ```
   score = 1.0
         - 0.20 * n_missing
         - 0.15 * n_conflicting
         - 0.10 * n_untestable
         - 0.10 * n_metric
         - 0.05 * n_ambiguous
   ```
3. Floor the score at 0.0.
4. Determine verdict:
   - `pass` if score >= 0.85
   - `revise` otherwise
5. Compose `trace` showing every term in the formula with the count, e.g.:
   `1.0 - 0.20*2 (missing) - 0.15*0 (conflicting) - 0.10*3 (untestable) - 0.10*1 (metric) - 0.05*4 (ambiguous) = 0.05`
6. Emit `{readiness_score, verdict, trace, confidence}`. Confidence is 0.97 when all counts came from machine-readable findings; lower if the findings array contained kinds outside the enums above.

## How to think
- The formula is fixed. Do not adjust weights for "perceived severity".
- An empty findings array yields a perfect 1.0 — that is correct.
- A finding with an unrecognised kind -> include it under the closest match for counting, but lower confidence and note it in trace.
- Verdict threshold is 0.85, matching the PRD readiness gate. Never relax it.
- This skill is mechanical. If you find yourself reasoning about content, you have over-stepped.

## Required inputs
`findings` must be an array (may be empty). Each element must have a `kind` string. If `findings` is missing or not an array, STOP and ask human.

## Output format
{
  "readiness_score": 0.0,
  "verdict": "pass|revise",
  "trace": "1.0 - 0.20*<n> - 0.15*<n> - 0.10*<n> - 0.10*<n> - 0.05*<n> = <result>",
  "confidence": 0.0
}

## Quality criteria
Passes if: counts match the input findings exactly; formula applied verbatim; floor at 0.0 honoured; verdict consistent with score threshold; trace is reproducible.
Fails if: weights tweaked; counts wrong; verdict inconsistent with score; trace missing terms.

## Common pitfalls
- Treating each `check-prd-completeness` finding (missing/empty/skeleton) with a different weight — they all count as `n_missing`.
- Forgetting to floor at 0.0 — a heavily defective PRD can produce negative arithmetic.
- Reporting a different threshold than 0.85.
- Editorialising in `trace` rather than emitting the literal formula.

## Examples
Good output:
{
  "readiness_score": 0.55,
  "verdict": "revise",
  "trace": "1.0 - 0.20*1 (missing) - 0.15*0 (conflicting) - 0.10*1 (untestable) - 0.10*1 (metric) - 0.05*1 (ambiguous) = 0.55",
  "confidence": 0.97
}

Good output (clean PRD):
{
  "readiness_score": 1.0,
  "verdict": "pass",
  "trace": "1.0 - 0.20*0 - 0.15*0 - 0.10*0 - 0.10*0 - 0.05*0 = 1.00",
  "confidence": 0.97
}

Bad output:
{
  "readiness_score": 0.9,
  "verdict": "pass",
  "trace": "felt close to ready"
} (formula not applied; trace not reproducible)

## Stop condition
Score computed, floored, verdict determined by 0.85 threshold, trace shows every term with counts and final result, confidence reported.

## Confidence guidance
Lower confidence when:
- Any finding has an unrecognised kind -> <= 0.92
- Findings array is unusually structured -> <= 0.90
- Mixed score sources beyond the five check skills -> <= 0.88
Confidence >= 0.95 is required to proceed without human review.
