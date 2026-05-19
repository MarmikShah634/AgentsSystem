# Claude Code Adapter

Claude Code reads from a `.claude/` directory in the project root.

## Layout produced by `scripts/sync-platforms.sh`

```
.claude/
├── agents/                # one .md per agent (mirrored from agents/)
├── skills/<id>/SKILL.md   # mirrored from skills/<cat>/<id>/SKILL.md
├── commands/              # mirrored from commands/
├── hooks/                 # symlinks/copies of hooks/*.sh
└── settings.json          # wires hooks to Claude Code events
```

## Installation

```bash
./scripts/sync-platforms.sh claude-code
# then symlink or copy platforms/claude-code/.claude into your project root
cp -R platforms/claude-code/.claude /path/to/your/project/.claude
```

## Hook wiring (settings.json)

The generated `settings.json` maps lifecycle scripts to Claude Code's
hook events:

| ADS hook | Claude Code event |
|----------|-------------------|
| `pre-task-plan.sh` | `UserPromptSubmit` |
| `confidence-gate.sh` | `Stop` |
| `post-task-log.sh` | `Stop` / `SubagentStop` |
| `post-edit-test.sh` | `PostToolUse` (Edit/Write) |
| `pre-commit-test.sh` | `PreToolUse` (Bash, when matching `git commit`) |

See `settings.json` for the actual matchers.
