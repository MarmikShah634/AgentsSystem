# Google Antigravity Adapter

Antigravity is an agent-first IDE. Agents are registered via an
`.antigravity/` directory at the project root containing YAML descriptors.

## Layout produced by `scripts/sync-platforms.sh`

```
.antigravity/
├── config.yaml            # registers all agents, skills, hooks
├── agents/<id>.yaml       # one per agent
├── skills/<id>.yaml       # one per skill
├── commands/<id>.yaml     # one per command
└── hooks/                 # mirrored from hooks/
```

## Installation

```bash
./scripts/sync-platforms.sh antigravity
cp -R platforms/antigravity/.antigravity /path/to/your/project/.antigravity
```

## Notes

- Each YAML descriptor references the canonical markdown body under
  `agents/` or `skills/` via a `source` field so there is no content
  duplication.
- Hooks are wired through `config.yaml` under the `lifecycle:` map.
