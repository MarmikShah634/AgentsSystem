# CODEX.md

This file supplements `SPEC.md` with OpenAI Codex CLI operational notes.

## Layout

`scripts/sync-platforms.sh codex` produces:

```
AGENTS.md           # consolidated description of all agents + skills + rules
.codex/
└── config.toml     # Codex CLI config (model, sandbox, approval policy)
```

`AGENTS.md` is the canonical source Codex reads. It is **fully
regenerated** from `agents/`, `skills/`, `commands/`, and `SPEC.md` on
every sync — never hand-edit.

## Caveman

Codex is in Caveman's auto-activate list. Once Caveman is installed it
applies automatically; no per-session command needed.

## Approval policy

`.codex/config.toml` sets `approval_policy = "on-request"` and
`sandbox.mode = "workspace-write"`. This is the Codex equivalent of the
orchestrator's confidence gate — Codex will pause for human approval
before applying changes, mirroring the `infra-confidence` floor.

## No structured hooks

Codex lacks a lifecycle-hook system. Wire the orchestrator's hooks via
git hooks instead:

```bash
ln -sf ../../hooks/pre-commit-test.sh .git/hooks/pre-commit
```

## Reading order

1. `AGENTS.md` (auto-loaded by Codex)
2. `SPEC.md`
3. `CODEX.md` (this file)
