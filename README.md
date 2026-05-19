# Agentic Development System

A tech-agnostic, orchestrator-managed ecosystem of specialized AI agents that
covers the **entire** software development lifecycle — from requirements
gathering through deployment — and works across **Claude Code**, **Cursor**,
**Google Antigravity**, and **OpenAI Codex**.

## Core Principles

1. **Single Responsibility** — One skill does one task. One agent owns one role.
2. **Plan Before Execute** — Every task is decomposed into a plan that agents
   must follow strictly. Plans are persisted and auditable.
3. **Confidence Gating** — Any agent action below 90% confidence escalates to a
   human via a gated prompt. No silent guessing.
4. **Audit Everything** — Every action is logged with the agent, task, inputs,
   outputs, confidence, and timestamps.
5. **Test-Backed** — Every implementation task is paired with a corresponding
   test task (unit + Puppeteer E2E where applicable).
6. **Tech Agnostic** — No assumption of language, framework, or stack. Adapters
   detect and adapt.
7. **Multi-Platform** — Same agent/skill specifications compile to native
   formats for Claude, Cursor, Antigravity, and Codex.

## Quickstart

```bash
# 1. Detect platform and sync agent definitions into native locations
./scripts/sync-platforms.sh

# 2. Initialise the orchestrator for the current project
python3 orchestrator/cli.py init

# 3. Kick off the lifecycle (requirements → deploy)
python3 orchestrator/cli.py run --goal "Build a TODO REST API"
```

## High-Level Lifecycle

```
[ Requirements ] → [ Architecture ] → [ Planning ] → [ Coding ] → [ Testing ]
        ↓                ↓                ↓             ↓             ↓
   user-story-     tech-stack-      task-decomp-   implement-   puppeteer-
   gathering       selection        ition          function     e2e-test
        ↓                ↓                ↓             ↓             ↓
                          [  Orchestrator  ]
                                   ↓
                     [ Review ] → [ Docs ] → [ Deploy ]
```

Each arrow is gated by:
- A persisted **plan** (in `logs/plans/`)
- A **confidence check** (≥0.90 to proceed, otherwise human-in-loop)
- An **audit log entry** (in `logs/audit/`)

## Directory Map

| Path | Purpose |
|------|---------|
| `orchestrator/` | Platform-agnostic core: planner, router, confidence gate, logger, registry |
| `agents/` | Agent role specs (markdown) — source of truth |
| `skills/` | Tiny single-task skills — source of truth |
| `commands/` | Slash command specs |
| `hooks/` | Lifecycle hook scripts |
| `platforms/claude-code/` | Compiled artifacts for Claude Code |
| `platforms/cursor/` | Compiled artifacts for Cursor |
| `platforms/antigravity/` | Compiled artifacts for Google Antigravity |
| `platforms/codex/` | Compiled artifacts for OpenAI Codex |
| `puppeteer/` | E2E browser test runner |
| `templates/` | Plan / log / spec templates |
| `scripts/` | Generators and sync utilities |
| `logs/` | Audit trail (plans + executions) |

## How Platform Sync Works

Source-of-truth lives in `agents/` and `skills/`. The `scripts/sync-platforms.sh`
script reads those and emits the right shape for each tool:

| Source | Claude Code | Cursor | Antigravity | Codex |
|--------|-------------|--------|-------------|-------|
| `agents/*.md` | `.claude/agents/*.md` | `.cursor/rules/agents/*.mdc` | `.antigravity/agents/*.yaml` | `AGENTS.md` section |
| `skills/**/SKILL.md` | `.claude/skills/<name>/SKILL.md` | `.cursor/rules/skills/<name>.mdc` | `.antigravity/skills/<name>.yaml` | referenced from `AGENTS.md` |
| `commands/*.md` | `.claude/commands/*.md` | `.cursor/commands/*.md` | `.antigravity/commands/*.yaml` | (none) |
| `hooks/*.sh` | `.claude/hooks/` + `settings.json` | `.cursor/hooks/` | `.antigravity/hooks/` | git hooks |

See `ARCHITECTURE.md` for the full design and `platforms/*/README.md` for the
per-tool wiring details.

## Confidence Gate

Every agent emits a structured response containing a `confidence` score in
`[0.0, 1.0]`. The orchestrator (or `hooks/confidence-gate.sh` when running
in-tool) blocks execution and prompts the user when:

- `confidence < 0.90`
- the task touches a flagged-sensitive surface (secrets, prod config, schema
  migrations, public APIs) — these are *always* human-gated regardless of
  confidence.

## License

MIT — use freely.
