---
id: generate-regression-test
category: testing
owner_agent: tester
inputs:
  - bug_report: "structured report with repro steps, expected, actual"
  - target_path: "optional file path of suspected fault location"
outputs:
  - test_file_path: "absolute path to the new failing test"
  - failure_log: "captured failure output proving the bug reproduces"
  - rationale: "1-3 sentences"
  - confidence: "float in [0,1]"
requires_plan: true
emits_confidence: true
confidence_floor: 0.85
---

# Skill: generate-regression-test

## Purpose
Write one test that reproduces the bug in `bug_report` and currently
fails for the documented reason. The failing test is the contract
handed to the coder's `fix-bug` skill. Anti-hallucination: never write
a test that passes on the broken code — that defeats the purpose.

## When to invoke
A bug report exists with at least: repro steps, expected behaviour,
actual behaviour. The repro is deterministic.
Do NOT invoke when: bug is "sometimes slow", repro requires production
data, or the failure mode is not yet isolated.

## Procedure (follow exactly)
1. Detect runner (see `generate-unit-test` rules). Place the test next
   to existing regression tests if a convention exists
   (`tests/regression/`, `__tests__/bugs/`, …); else colocate with
   target.
2. Translate repro steps into the smallest possible test: minimal
   setup, the exact action, an assertion on the expected outcome.
3. Name the test after the bug ID/ticket (e.g.
   `test_bug_1234_negative_amount_rejected`).
4. Run the test once against the current (broken) code. Capture the
   failure log. The failure message MUST match the actual behaviour
   from the bug report — not a setup error, not an import error.
5. If it fails for the wrong reason, fix the test until it fails for
   the right reason. Do not modify source code in this skill.

## How to think
- Failure unrelated to the bug (e.g. `ImportError`) → fix the test
  scaffold, do not declare success.
- Repro requires network → record/fixture the response; do not hit
  live endpoints.
- Race condition → make the test deterministic via injected clock or
  controlled scheduler; if you cannot, STOP and lower confidence.
- Bug only repros in prod data → STOP, escalate for a fixture.

## Required inputs
Repro steps must be runnable in a test environment. Expected and
actual must differ unambiguously.

## Output format
```json
{"test_file_path": "/abs/path/test_bug_1234.py",
 "failure_log": "AssertionError: expected 0, got -42",
 "rationale": "Reproduces negative amount accepted in cart.",
 "confidence": 0.0}
```

## Quality criteria
Pass: test currently red; failure message names the right symptom; no
flakiness across 3 reruns; no source files touched.
Fail: test green on broken code; failure caused by missing fixture;
test asserts implementation detail instead of bug symptom.

## Common pitfalls
- Asserting on log text that may change after fix.
- Using `pytest.raises(Exception)` — be specific.
- Skipping the rerun-to-confirm-failure step.
- Touching source "just to make the test runnable".

## Examples
Pass (pytest):
```python
def test_bug_1234_negative_amount_rejected():
    with pytest.raises(ValueError, match="non-negative"):
        Cart().add(item, qty=-1)
```
Fail: `def test_bug_1234(): assert True  # TODO after fix` — passes on
broken code.

## Stop condition
Test file exists; runner executes it; it fails; failure log matches
bug report's "actual" line; no source modified.

## Confidence guidance
Repro non-deterministic ≤0.7; failure mode unclear ≤0.65; requires
prod data ≤0.5; runner ambiguous ≤0.75. Must be ≥0.85 to emit.
