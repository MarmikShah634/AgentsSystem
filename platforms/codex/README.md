# OpenAI Codex Adapter

The Codex CLI honours an `AGENTS.md` file at the repo root, along with
`~/.codex/config.toml` for global settings. Codex does not currently expose
a structured "agents" registry the way Claude Code does — instead, every
agent role, skill, and lifecycle rule is described in prose inside
`AGENTS.md`, which Codex injects into the model's context.

## Layout produced by `scripts/sync-platforms.sh`

```
AGENTS.md            # consolidated description of all agents + skills + rules
.codex/
└── config.toml      # Codex CLI config (model, sandbox, approval policy)
```

## Installation

```bash
./scripts/sync-platforms.sh codex
cp platforms/codex/AGENTS.md       /path/to/your/project/AGENTS.md
cp -R platforms/codex/.codex       /path/to/your/project/.codex
```

## Hook wiring

Codex does not expose lifecycle hooks. Wire `hooks/*.sh` into git hooks
(`.git/hooks/pre-commit`) and rely on Codex's `approval_policy` for the
human-gate behaviour. Sample mapping is shown in the generated
`AGENTS.md`.
