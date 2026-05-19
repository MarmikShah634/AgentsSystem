---
id: lint-check
category: review
owner_agent: reviewer
inputs:
  - target_paths: "list of file/dir paths to lint (relative to repo_root)"
  - repo_root: "absolute path to repository root"
  - config_path: "optional explicit linter config path"
outputs:
  - findings: "list of {path, line, column, rule, severity, msg}"
  - verdict: "pass | changes-requested"
  - tool_used: "eslint|ruff|clippy|golangci-lint|rubocop|..."
  - confidence: "float in [0,1]"
requires_plan: true
emits_confidence: true
confidence_floor: 0.85
---

# Skill: lint-check

## Purpose
Run the repository's configured linter over `target_paths` and emit a
normalised finding list. Do not auto-fix; report only.

## When to invoke
Plan step is `lint` OR any patch touching source files before `code-review`.
Skip for docs-only or asset-only changes.

## Procedure (follow exactly)
1. Detect linter from project files:
   - `.eslintrc*` / `eslint.config.*` → `eslint --format json`.
   - `pyproject.toml` with `[tool.ruff]` or `ruff.toml` → `ruff check
     --output-format json`.
   - `Cargo.toml` → `cargo clippy --message-format=json -- -D warnings`.
   - `.golangci.yml` → `golangci-lint run --out-format json`.
   - `.rubocop.yml` → `rubocop --format json`.
2. Invoke with `target_paths` only — never `--fix`, never global scope.
3. Parse JSON output; normalise to {path, line, column, rule, severity, msg}.
4. Verdict: any `error` severity → `changes-requested`; warnings only →
   `pass` with findings attached.
5. Return non-zero linter exit code as `verdict: changes-requested`, never
   swallow it.

## How to think
- Linter rule disabled in config → respect it; do not re-flag.
- Generated files (e.g. `dist/`, `*.pb.go`) → exclude unless explicitly in
  `target_paths`.
- Linter crashes due to parse error → record as `error` severity finding
  pointing at the offending file:line.
- Auto-fixable rule → still report; the fix is a separate skill.

## Required inputs
`target_paths` non-empty; `repo_root` set. If no linter is configured, STOP
and return `verdict: pass` with `tool_used: "none"` and confidence 0.5.

## Output format
```json
{
  "findings": [
    {"path":"src/api/users.ts","line":42,"column":7,
     "rule":"@typescript-eslint/no-unused-vars","severity":"error",
     "msg":"'req' is defined but never used."},
    {"path":"src/api/users.ts","line":88,"column":3,
     "rule":"no-console","severity":"warning",
     "msg":"Unexpected console statement."}
  ],
  "verdict": "changes-requested",
  "tool_used": "eslint",
  "confidence": 0.92
}
```

## Quality criteria
Pass: every finding has rule id; severity preserved from linter; verdict
matches severity distribution; only `target_paths` scanned.
Fail: invented rule ids, dropping column info, treating warnings as errors,
running auto-fix.

## Common pitfalls
- Running linter from wrong cwd, picking up wrong config.
- Mapping linter severity inconsistently (`error` vs `2` vs `high`) — pick a
  single normalised vocabulary and stick to it.
- Suppressing output when linter exits non-zero without findings (config
  error) — must surface this.

## Examples
✅ `ruff check src/` emits
`{"path":"src/foo.py","line":3,"rule":"F401","severity":"error","msg":"`os`
imported but unused"}`.
❌ Reporting `{"rule":"unused-import"}` (non-canonical id) when ruff emits
`F401`.

## Stop condition
Linter ran on every target path; findings normalised; verdict set; exit code
honoured.

## Confidence guidance
Linter present, config detected, exit code 0 or 1 ≥0.9; linter missing 0.5;
linter crashed ≤0.6 (escalate). Floor 0.85 to emit `pass`.
