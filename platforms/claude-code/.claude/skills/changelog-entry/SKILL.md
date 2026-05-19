---
id: changelog-entry
category: docs
owner_agent: docs
inputs:
  - plan_id: "identifier of the plan/PR this change implements"
  - patch_summary: "1-2 sentence user-visible summary"
  - change_kind: "Added|Changed|Deprecated|Removed|Fixed|Security"
  - changelog_path: "path to CHANGELOG.md (default: CHANGELOG.md at repo root)"
  - version: "optional target version header, e.g. 1.4.0"
outputs:
  - changelog_entry: "the exact line(s) appended"
  - touched_paths: "[changelog_path]"
  - confidence: "float in [0,1]"
requires_plan: true
emits_confidence: true
confidence_floor: 0.85
---

# Skill: changelog-entry

## Purpose
Append a single Keep-a-Changelog entry under the appropriate section for
the upcoming release. One line per user-visible change, referencing the
plan id.

## When to invoke
Plan step is `changelog` OR a user-visible change is merging AND the repo
has a `CHANGELOG.md`. Skip for internal refactors, test-only changes,
docs-only edits.

## Procedure (follow exactly)
1. Read `changelog_path`. Confirm it follows Keep-a-Changelog format
   (sections: Added/Changed/Deprecated/Removed/Fixed/Security under an
   `## [Unreleased]` or version header).
2. Locate the target version block (`[Unreleased]` if `version` not
   provided; else create the version block at top if missing).
3. Locate or create the subsection matching `change_kind`.
4. Append exactly one bullet:
   `- <patch_summary> (#<plan_id>)`
   - Imperative voice ("Add", "Fix", "Remove"), past-tense allowed if file
     convention uses it — match the file.
   - One sentence, ≤120 chars where possible.
5. Preserve existing entries, ordering, and blank lines.

## How to think
- Multi-part change → one bullet per user-visible facet, all under the same
  plan id.
- Breaking change → use `Changed` or `Removed`; prefix bullet with
  `**BREAKING:**` if file convention uses it.
- Security fix → use `Security` section; never reference CVE details that
  aren't yet public.
- No CHANGELOG.md exists → STOP; do not bootstrap one without explicit
  instruction.

## Required inputs
All four core inputs non-empty. If `change_kind` is unclear, STOP and ask —
do not guess between `Changed` and `Fixed`.

## Output format
```json
{
  "changelog_entry": "- Add `LOG_LEVEL` env var to control logger verbosity (#PLAN-142)",
  "touched_paths": ["CHANGELOG.md"],
  "confidence": 0.95
}
```

## Quality criteria
Pass: one bullet appended in correct section; format matches surrounding
entries; plan id present; file still parses; no other lines edited.
Fail: rewriting prior entries, mixing `Added` with `Fixed`, omitting plan
id, breaking heading levels, multi-line bullets without continuation
indent.

## Common pitfalls
- Adding entries under a released version block.
- Duplicating an entry already present.
- Marketing voice ("we are excited to introduce…") — keep it factual.
- Referencing internal implementation details rather than user impact.

## Examples
✅ `- Fix race condition when two clients delete the same draft (#PLAN-77)`
under `### Fixed` of `## [Unreleased]`.
❌ `- refactored DraftService to use a mutex` under `### Added` — internal
detail in wrong section.

## Stop condition
Bullet present in correct section; file diff is exactly the added bullet
(plus any new section header if created); touched_paths is single file.

## Confidence guidance
Section exists and change_kind clear ≥0.95; new section created ≥0.9;
ambiguous kind or breaking-change classification ≤0.75 (escalate). Floor
0.85.
