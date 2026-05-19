# ANTIGRAVITY.md

This file supplements `SPEC.md` with Google Antigravity operational notes.
Antigravity reads from `.antigravity/` at the project root.

## Layout

`scripts/sync-platforms.sh antigravity` produces:

```
.antigravity/
├── config.yaml            # top-level registry + hook wiring
├── agents/<id>.yaml       # one per agent (references the source .md)
├── skills/<id>.yaml       # one per skill (references the source SKILL.md)
├── commands/<id>.yaml     # one per slash-command
└── hooks/                 # mirrored from /hooks
```

Each YAML descriptor references the canonical markdown body by `source:`
so there is no content duplication. `config.yaml` registers the agent and
skill directories and binds lifecycle hooks under `lifecycle:`.

## Caveman

Antigravity is not in Caveman's auto-activate list. Use the manual route:

1. Install once via `scripts/install-caveman.sh`.
2. In each Antigravity session, run `/caveman full`.

Or wire `session-start-caveman.sh` to Antigravity's `lifecycle.pre_task`
slot (see `config.yaml`).

## Confidence + sensitive surfaces

`config.yaml` sets `confidence_floor: 0.85` and declares the same
sensitive globs as `SPEC.md` §4. Antigravity agents are expected to honour
both.
