# Contributing

Adding agents, skills, hooks, or commands is mostly mechanical — but the
single-responsibility rules below are **binding**. Submissions that
violate them will be rejected.

## Read first

- `SPEC.md` — the binding system spec.
- `ARCHITECTURE.md` — how the orchestrator + infra agents fit together.
- The host-specific file for the tool you're testing against
  (`CLAUDE.md` / `CURSOR.md` / `ANTIGRAVITY.md` / `CODEX.md`).

## Golden rules

1. **One skill, one task.** A `SKILL.md` describes a single observable
   outcome. If you find yourself writing "and also …", split.
2. **One agent, one role.** Don't add a skill to an existing agent if it
   conflicts with the agent's role label. Add a new agent instead.
3. **250 lines max per `SKILL.md`.** `validate-system.sh` enforces this.
4. **Every coding step needs a test pair.** `infra-planner` rejects plans
   that violate this.
5. **Sensitive surfaces stay sensitive.** Touch `secrets/**`, `infra/**`,
   `migrations/**`, `**/.env*`, `**/Dockerfile`, `**/*.tf`, `docs/prd/**`,
   `docs/tsd/**`, `docs/sprints/**` only via the agent that owns them
   (see `orchestrator/infra/confidence.py:DEFAULT_OWNERSHIP`).
6. **No multi-platform forks.** Edit source-of-truth only (`agents/`,
   `skills/`, `commands/`, `hooks/`), then run
   `./scripts/sync-platforms.sh` to regenerate `platforms/`.
7. **Tests required.** Every new module under `orchestrator/` and every
   new agent goes with at least one test under `tests/`.

## Adding a skill

```bash
./scripts/new-skill.sh <category> <skill-id> <owner-agent>
```

This scaffolds `skills/<category>/<skill-id>/SKILL.md` with the canonical
frontmatter. Edit the **Task** and **Stop condition** sections. Keep both
short — the LLM hosting this skill will read it on every invocation.

## Adding an agent

1. Create `agents/<id>.md` with frontmatter:
   - `id`, `role`, `owns` (skill globs), `hands_off_to`,
     `confidence_floor`, `sensitive_surfaces`.
2. List the agent's owned skills under `skills/<category>/<skill-id>/`.
3. If the agent legitimately writes a sensitive surface, register
   ownership in `orchestrator/infra/confidence.py:DEFAULT_OWNERSHIP`.
4. Add a test to `tests/` confirming the agent loads and owns its skills.

## Adding a hook

1. Write the script under `hooks/<name>.sh` with a shebang and proper
   exit codes (see existing scripts for the convention).
2. Wire it into the relevant platform inside `scripts/sync-platforms.sh`.
3. Mark it `chmod +x`.

## Adding a slash command

1. Create `commands/<id>.md` with frontmatter `id`, `description`,
   `entry_agent`.
2. The body describes the sequence of agents the command invokes.

## Before you push

```bash
python3 -m pytest tests/ -q
./scripts/validate-system.sh
./scripts/sync-platforms.sh   # commit the platforms/ diff too
```

## Out of scope for this repo

- Per-customer or per-tenant agent variants — keep agents generic.
- Hardcoded model names. Adapters configure those; agents don't.
- New top-level directories. Get an issue approved first.
