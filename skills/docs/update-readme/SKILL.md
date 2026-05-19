---
id: update-readme
category: docs
owner_agent: docs
inputs:
  - patch: "unified diff of code changes"
  - readme_path: "path to README (default: README.md at repo root)"
  - surfaces_changed: "list of {kind, name} where kind ∈ cli|api|env|config|install"
outputs:
  - doc_changes: "list of patches to README sections (empty if nothing to update)"
  - touched_paths: "list of modified files"
  - rationale: "1-2 sentence explanation"
  - confidence: "float in [0,1]"
requires_plan: true
emits_confidence: true
confidence_floor: 0.85
---

# Skill: update-readme

## Purpose
Update README only when a user-visible documented surface changes. Avoid
churn — if nothing documented changed, emit `doc_changes: []`.

## When to invoke
Plan step is `update-docs` OR patch adds/removes/renames CLI flags, public
API endpoints, environment variables, config keys, install steps, or
supported platforms.
Do NOT invoke for: internal refactors, private helpers, test-only changes,
dependency bumps without behaviour change.

## Procedure (follow exactly)
1. Read current README. Identify sections (Install, Usage, Configuration,
   CLI, API, Environment).
2. For each entry in `surfaces_changed`, locate the matching section. No
   section exists → create one only if the surface is user-facing.
3. Update only the affected lines. Preserve heading levels, link anchors,
   and example formatting (code fences, language tags).
4. If a flag/env var was removed, remove the doc entry AND add a "Removed
   in vX.Y" note if a versioning convention is evident in the README.
5. Run a final read-through: every documented surface still exists in code;
   every new surface in `surfaces_changed` appears in the README.

## How to think
- Internal-only surface (e.g. private function) → do nothing.
- Surface renamed → update the doc, add a one-line deprecation note if the
  README already follows that style; otherwise just update.
- Multiple readmes (monorepo) → update only the one at `readme_path`.
- README is auto-generated (banner says so) → STOP and route to
  `generate-api-docs` instead.

## Required inputs
`patch` non-empty; `readme_path` exists. If `surfaces_changed` is empty,
emit `doc_changes: []` and exit with confidence 0.95.

## Output format
```json
{
  "doc_changes": [
    {"path":"README.md","section":"## Environment",
     "diff":"+ - `LOG_LEVEL` — one of `debug|info|warn|error`. Default `info`."}
  ],
  "touched_paths": ["README.md"],
  "rationale": "Added LOG_LEVEL env var in patch; documented under Environment.",
  "confidence": 0.9
}
```

## Quality criteria
Pass: every changed surface reflected; no unrelated edits; formatting
preserved; no broken links; no stale code samples.
Fail: rewriting unrelated prose, changing tone, fabricating surfaces,
introducing TODO markers, duplicating sections.

## Common pitfalls
- Updating README when no public surface changed (churn).
- Copying internal class names into Usage examples.
- Breaking anchor links by renaming a heading.
- Missing the table of contents update.

## Examples
✅ Patch adds CLI flag `--dry-run`; doc_changes appends `- --dry-run — print
actions without executing` under `## CLI`.
❌ Patch refactors an internal helper; doc_changes adds a paragraph about
the helper class.

## Stop condition
Every entry in `surfaces_changed` mapped to a README edit (or explicitly
deferred); README still parses as Markdown; touched_paths lists only README
files.

## Confidence guidance
Surfaces explicit and small ≥0.9; auto-generated README detected → 0.5
(route to generate-api-docs); ambiguous surface ≤0.7. Floor 0.85.
