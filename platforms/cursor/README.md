# Cursor Adapter

Cursor reads project rules from `.cursor/rules/*.mdc` (and commands from
`.cursor/commands/`). Each `.mdc` file is markdown with YAML frontmatter
that controls when Cursor attaches the rule.

## Layout produced by `scripts/sync-platforms.sh`

```
.cursor/
├── rules/
│   ├── agents/<id>.mdc    # one per agent
│   └── skills/<id>.mdc    # one per skill
├── commands/<id>.md       # one per command
└── hooks/                 # mirrored from hooks/  (invoked manually or via tasks)
```

## Installation

```bash
./scripts/sync-platforms.sh cursor
cp -R platforms/cursor/.cursor /path/to/your/project/.cursor
```

## Notes

- Cursor does not have a native hook system as of writing. The orchestrator
  invokes hooks itself when Cursor is the host; the scripts under
  `.cursor/hooks/` are kept so they can be wired into VS Code tasks or
  pre-commit.
- The `.mdc` `globs` / `alwaysApply` fields determine when each rule is
  injected into the model's context.
