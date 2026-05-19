---
id: check-prd-testability
category: prd
owner_agent: prd-reviewer
inputs:
  - prd_path: "absolute path to the PRD file under docs/prd/"
outputs:
  - findings: "list of {section, kind: 'untestable', msg, fix} entries, one per offending FR/NFR"
  - verdict: "'pass' if zero untestable items else 'revise'"
  - readiness_score: "float in [0,1] for this dimension"
  - confidence: "float in [0,1]"
requires_plan: true
emits_confidence: true
confidence_floor: 0.95
---

# Skill: check-prd-testability

## Purpose
Audit every Functional Requirement and Non-Functional Requirement for testability. An item is testable when its outcome is observable from outside the system and (for NFRs) carries a number or named standard. Emit findings; never rewrite.

## When to invoke
Invoke after `check-prd-completeness` passes (or after FR and NFR sections are confirmed present). Run before scoring readiness.

Do NOT invoke to: enforce numbering format (that is completeness), find conflicts (use check-prd-conflicts), or score metrics quality (use check-prd-metrics-quality).

## Procedure (follow exactly)
1. Read `prd_path`. Extract the Functional Requirements list and Non-Functional Requirements list.
2. For each FR, flag `untestable` if any of:
   a. Uses subjective adjectives without numbers ("fast", "intuitive", "easy", "robust", "scalable").
   b. Lacks an observable trigger (no "when <event>" clause or the trigger is "as needed", "appropriately").
   c. References internal state with no external symptom ("the system SHALL index records").
   d. Uses weak verbs ("should", "may", "could") instead of SHALL.
3. For each NFR, flag `untestable` if any of:
   a. No number AND no named standard (WCAG 2.2 AA, SOC2, FERPA, etc.).
   b. Subjective claim ("highly secure") not backed by a measurable outcome.
   c. Compound NFR mixing two categories without separable metrics.
4. For each flagged item, emit a finding with kind `untestable` and a concrete `fix` rewrite suggestion (one sentence) — the fix is advice, not an authored replacement.
5. Verdict `pass` iff zero findings. Otherwise `revise`.
6. `readiness_score` = 1.0 - 0.1 * count(findings), floor 0.0.

## How to think
- Borderline subjective adjective with adjacent number -> testable; do not flag.
- Internal-sounding behavior with externally observable symptom -> rewrite the FR mentally; if the symptom IS observable, it's testable even if poorly phrased; flag only if no symptom exists.
- NFR cites a named standard (e.g. WCAG 2.2 AA) without a number -> testable; the standard is the metric.
- Multiple offenses in one FR -> single finding listing each, not multiple findings on the same id.
- NEVER rewrite the PRD. The `fix` is a recommendation only.

## Required inputs
`prd_path` readable; FR and NFR sections present. If either section is missing, STOP and route back to check-prd-completeness first.

## Output format
{
  "findings": [
    {"section": "Functional Requirements|Non-Functional Requirements", "kind": "untestable", "msg": "FR-3 uses 'intuitive' with no numeric threshold", "fix": "Replace with a measurable outcome, e.g. 'p95 task completion < 60s on first attempt'"}
  ],
  "verdict": "pass|revise",
  "readiness_score": 0.0,
  "confidence": 0.0
}

## Quality criteria
Passes if: every FR and NFR examined; offenses precisely cited with item id; fixes are concrete one-sentence suggestions; verdict and score consistent.
Fails if: items skipped; vague findings without item ids; PRD modified; kinds outside `untestable`.

## Common pitfalls
- Flagging an FR that references an internal data store but produces an observable user-visible result.
- Missing weak-verb violations because the sentence "sounds" formal.
- Flagging an NFR that cites WCAG 2.2 AA as numberless.
- Suggesting fixes that introduce tech ("use Cypress to test it").

## Examples
Good finding:
{"section": "Functional Requirements", "kind": "untestable", "msg": "FR-5 says 'the system should feel responsive' — weak verb and subjective.", "fix": "Use SHALL with a measurable trigger and outcome, e.g. 'the system SHALL respond to a click within 200ms p95'."}

Good finding:
{"section": "Non-Functional Requirements", "kind": "untestable", "msg": "NFR-2 'scalable for many users' has no peak-load number.", "fix": "State a peak number, e.g. '50,000 concurrent sessions during 8-9am'."}

Bad finding:
{"section": "Functional Requirements", "kind": "weak", "msg": "I rewrote FR-5", "fix": "..."} (kind invented, rewrites)

## Stop condition
Every FR and NFR examined; findings emitted only for offenders; verdict and readiness_score consistent with findings; confidence reported.

## Confidence guidance
Lower confidence when:
- Adjectives are borderline-subjective and judgment-heavy -> <= 0.9
- Standards mentioned but versions ambiguous -> <= 0.9
- FR phrasing suggests external symptom but doesn't state it -> <= 0.85
- NFR mixes categories making evaluation ambiguous -> <= 0.85
Confidence >= 0.95 is required to proceed without human review.
