---
id: start-bugfix
description: "Regression-test-first bugfix flow"
entry_agent: planner
---

# /start-bugfix

**Usage:** `/start-bugfix <bug-description>`

Bugfix flow. The defining invariant: a failing regression test exists
BEFORE any fix lands. The planner enforces this by sequencing the steps
below in order.

## Preconditions

- The bug description names: symptom, reproduction steps, expected vs.
  actual outcome.
- The repo's test suite currently passes (otherwise we cannot tell what
  the new regression broke).
- If the bug touches a sensitive surface, the human gate fires at step 4
  regardless of confidence.

If the bug description lacks reproduction steps, STOP and ask the human.

## Sequence

1. `planner` → `decompose-task` + `sequence-dependencies` — emits at
   least the four steps below, with the test step pairing the fix step.
2. `tester` → `generate-regression-test` — writes a test that fails
   against current code AND fails for the correct reason (run once to
   confirm). If the test passes against current code, the bug isn't a
   bug; halt and ask the human.
3. Router determines tier by inspecting which files would change:
   - UI-tier paths → `frontend` → `fix-frontend-bug`
   - Server-tier paths → `backend` → `fix-backend-bug`
   - Both tiers → emit two paired fix steps in dependency order
4. `tester` → `run-tests` — the regression test now passes; ALL other
   tests remain green. Any flake or unrelated breakage halts the flow.
5. `reviewer` → `code-review` — checks the fix is minimum-diff and does
   not refactor surrounding code.
6. `security` → `security-scan` + `secret-scan` — runs on every patch.
7. `accessibility-auditor` (UI fixes) — runs all five WCAG checks.
8. `performance-auditor` (perf-sensitive fixes) — re-runs the budget
   audit on the affected surface.
9. `docs` → `changelog-entry` — one line per user-visible fix.

## Gating

- `infra-confidence` fires at every step. Floor 0.85; reviewers/auditors
  at 0.95.
- The fix step is BLOCKED until the regression test exists and is
  confirmed failing. The orchestrator does not skip step 2 even if the
  agent claims it knows the fix.
- Sensitive-surface touches escalate to human regardless of confidence.
