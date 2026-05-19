---
id: start-bugfix
description: "Kick off a bugfix flow — regression test first, then fix"
entry_agent: planner
---

# /start-bugfix

**Usage:** `/start-bugfix <bug-description>`

Sequence:

1. `planner` → `decompose-task` (emits at least these steps)
2. `tester` → `generate-regression-test` (must fail)
3. `frontend` → `fix-frontend-bug` OR `backend` → `fix-backend-bug`
   (router picks based on `touched_paths`)
4. `tester` → `run-tests` (regression now passes; everything else green)
5. `reviewer` → `code-review`
6. `security` → `security-scan`
7. `docs` → `changelog-entry`
