# CURSOR.md

This file supplements `SPEC.md` with Cursor-specific operational notes.
Cursor reads project rules from `.cursor/rules/*.mdc`.

## Layout

`scripts/sync-platforms.sh cursor` produces:

```
.cursor/
├── rules/
│   ├── agents/<id>.mdc    # one per agent
│   └── skills/<id>.mdc    # one per skill
├── commands/<id>.md       # one per slash-command
└── hooks/                 # mirrored from /hooks
```

Each `.mdc` file has YAML frontmatter that controls when Cursor attaches
it (`alwaysApply`, `globs`).

## Caveman

Cursor does not auto-activate Caveman. The installer
(`scripts/install-caveman.sh`) runs `caveman --with-init`, which emits a
rule file at `.cursorrules` (or under `.cursor/rules/`) that Cursor will
pick up automatically.

## No native hooks

Cursor lacks a structured hook system. The orchestrator-side hooks under
`/hooks` still run when the orchestrator drives Cursor; the
`.cursor/hooks/` copies are kept so VS Code tasks or git hooks can fire
them out of band.

For pre-commit testing, install a git hook:

```bash
cp hooks/pre-commit-test.sh .git/hooks/pre-commit
chmod +x .git/hooks/pre-commit
```

## Reading order in Cursor

1. `.cursor/rules/agents/<id>.mdc`
2. `.cursor/rules/skills/<id>.mdc`
3. `SPEC.md`

The rule frontmatter (`alwaysApply: false`, `globs: ["**/*"]`) keeps
context lean — only relevant rules attach per file.
