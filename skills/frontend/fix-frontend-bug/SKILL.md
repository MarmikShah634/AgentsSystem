---
id: fix-frontend-bug
category: frontend
owner_agent: frontend
inputs:
  - bug_report: "user-visible symptom + reproduction steps"
  - failing_puppeteer_test: "path to the regression test that currently fails"
  - suspected_paths: "optional: list of UI files implicated in the report"
outputs:
  - patch: "unified diff of changes"
  - touched_paths: "list of files modified"
  - rationale: "1-3 sentences explaining root cause"
  - confidence: "float in [0,1]"
requires_plan: true
emits_confidence: true
confidence_floor: 0.85
---

# Skill: fix-frontend-bug

## Purpose
Apply the minimum-diff fix for a UI bug so that the supplied failing Puppeteer/Playwright test turns green while every previously-green test stays green.

## When to invoke
Invoke when the plan step is fix a UI bug AND `failing_puppeteer_test` exists and currently fails AND the failure reproduces locally. Reject if the test is missing — request `generate-regression-test` first. Reject if the suspected fault is server-tier.

## Procedure (follow exactly)
1. Run `failing_puppeteer_test`. Confirm it fails for the reason described in `bug_report`. If it fails for a different reason, STOP and revisit the test.
2. Locate the offending code. Prefer `suspected_paths`; otherwise trace from the test selector through component tree.
3. Form a one-sentence root cause hypothesis. Write it in `rationale`. If you cannot, STOP — do not patch blindly.
4. Apply the smallest fix that addresses the root cause. Forbidden: changing the test, masking with `try/catch`, hiding the element, or adding `setTimeout`.
5. Run the full UI test suite + screenshot diff. The target test must now pass; all others must remain green.
6. If the fix touches a shared component, ensure every callsite still renders unchanged (screenshot diff <1%).

## How to think
- "Works on my machine" → reproduce in the same browser+viewport the Puppeteer test uses; do not dismiss.
- Race condition → fix the cause (await the correct promise), not the symptom (sleep).
- Off-by-one in pagination → patch the math, not the test fixture.
- Tempted to refactor surrounding code → don't; emit a follow-up `refactor-frontend` step.

## Required inputs
`bug_report` and `failing_puppeteer_test` non-empty. `suspected_paths` may be empty.

## Output format
{"patch": "unified diff", "touched_paths": ["src/components/UserList.tsx"], "rationale": "1-3 sentences explaining root cause and fix", "confidence": 0.0}

## Quality criteria
Passes if: regression test now passes; all prior tests still green; diff scoped to root-cause file(s); no `setTimeout`/`sleep` hack; no test file altered; no server file altered.
Fails if: modifies the failing test; broadens a `catch` to mask the error; hides UI to bypass assertion; touches more files than necessary; introduces a dependency.

## Common pitfalls
- Adding `await page.waitForTimeout(500)` in the test to "stabilize" it. Forbidden — fix the race.
- Wrapping the buggy line in `try {} catch {}`. Masking, not fixing.
- Reformatting the whole file. Inflates diff.

## Examples
React fix for a stale-closure bug:
```tsx
// before
useEffect(() => { fetchData().then(setData); }, []);          // misses prop changes
// after
useEffect(() => { fetchData(userId).then(setData); }, [userId]);
```

Anti-pattern (masking):
```tsx
// before: throws when list is empty
return items[0].name;
// "fix":
try { return items[0].name; } catch { return ''; }            // hides the bug
// proper fix:
if (items.length === 0) return <EmptyState />;
return items[0].name;
```

## Stop condition
`failing_puppeteer_test` passes; full UI suite passes; screenshot diff <1% on unrelated views; `touched_paths` is the smallest set required.

## Confidence guidance
Lower when: root cause uncertain (≤0.7), failure not reproduced locally (≤0.6), fix touches shared component (≤0.8), test flake suspected (≤0.7). Floor 0.85 to proceed.
