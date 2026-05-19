# CLAUDE.md (Claude Code)

This file is read by Claude Code at session start. It supplements `SPEC.md`
with Claude-specific operational notes.

## Skill, agent, command, hook discovery

Claude Code reads agents and skills from `.claude/` in the project root.
The canonical source is `agents/`, `skills/`, `commands/`, `hooks/` at the
repo root; `scripts/sync-platforms.sh claude-code` regenerates
`.claude/` from those.

| Source | Claude location |
|---|---|
| `agents/*.md` | `.claude/agents/*.md` |
| `skills/**/SKILL.md` | `.claude/skills/<id>/SKILL.md` |
| `commands/*.md` | `.claude/commands/*.md` |
| `hooks/*.sh` | `.claude/hooks/*.sh` + wiring in `.claude/settings.json` |

## Hook wiring

The generated `.claude/settings.json` wires:

| ADS hook | Claude Code event |
|---|---|
| `session-start-caveman.sh` | `SessionStart` (Caveman auto-activation) |
| `pre-task-plan.sh` | `UserPromptSubmit` |
| `post-edit-test.sh` | `PostToolUse` matcher `Edit\|Write` |
| `pre-commit-test.sh` | `PreToolUse` matcher `Bash`, guarded on `git commit` |
| `post-task-log.sh` + `confidence-gate.sh` | `Stop` |

## Subagent delegation

When this CLAUDE.md is in effect, treat every entry in `agents/` as an
invokable subagent. Use the `Agent` tool with `subagent_type` set to the
agent's `id` field (frontmatter). The orchestrator's `route-step` skill
is the canonical entry point; direct invocation is reserved for cases
where the plan explicitly delegates to a subagent.

## Slash commands available

- `/start-product <one-liner>` — full PRD-first lifecycle.
- `/start-feature <goal>` — feature flow assuming PRD/TSD exist.
- `/start-bugfix <description>` — regression-test-first bugfix.
- `/design-review <path>` — designer audit.
- `/ship-it <env>` — build + security + deploy.
- `/plan <goal>` — generate a plan only.
- `/status` — today's audit summary.

## Caveman

Caveman activates at SessionStart via the hook. Useful inline commands:

- `/caveman lite|full|ultra|wenyan` — change mode mid-session.
- `/caveman-commit` — compress commit message.
- `/caveman-review` — compress code review output.
- `/caveman-stats` — see savings so far.

If Caveman isn't installed, the session-start hook fails open with a
warning; install once via `scripts/install-caveman.sh`.

## Sensitive surfaces (Claude must NEVER touch without human approval)

See `SPEC.md` §4. Claude Code's hook system enforces this via
`confidence-gate.sh`; do not bypass.
