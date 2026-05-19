# Logs

- `plans/<uuid>.json` — every plan ever generated. Append-only.
- `audit/<YYYY-MM-DD>.jsonl` — one JSONL record per agent step.

These are gitignored by default (see `.gitignore`) — they contain
project-specific run data, not source-of-truth. Strip the `*` line in
`.gitignore` if you want plans tracked in version control.
