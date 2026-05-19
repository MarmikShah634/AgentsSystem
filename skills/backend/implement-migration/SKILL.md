---
id: implement-migration
category: backend
owner_agent: backend
inputs:
  - description: "short label for the migration, e.g. add_users_table"
  - up_sql_or_ops: "forward operations (autogenerate diff or explicit ops)"
  - down_sql_or_ops: "reverse operations that fully revert up"
  - target_environment: "dev|staging|prod — for human-gate severity"
outputs:
  - patch: "unified diff containing the new migration file"
  - touched_paths: "list of files created/modified"
  - migration_path: "path to the new migration file"
  - rationale: "1-3 sentences"
  - confidence: "float in [0,1]"
  - human_gate: "true — migrations always require human approval before apply"
requires_plan: true
emits_confidence: true
confidence_floor: 0.85
---

# Skill: implement-migration

## Purpose
Author one forward + reverse database migration using the project's existing migration tool. Migrations are sensitive: this skill emits the file but always sets `human_gate: true`; the harness must not auto-apply.

## When to invoke
Invoke when the plan step is implement a migration AND the paired data-model change (if any) is already merged or in the same patch AND the project already has a migration tool configured. Reject if `down_sql_or_ops` is empty — irreversible migrations require explicit human override.

## Procedure (follow exactly)
1. Identify the migration tool: Alembic (Python), Prisma Migrate, ActiveRecord, Flyway, Goose, sqlx-cli, Knex. Reuse it; do not introduce a new tool.
2. Generate a new migration file via the tool's CLI so the timestamp/sequence is correct:
   - alembic → `alembic revision -m "<description>" --autogenerate` (or non-autogenerate if ops are explicit).
   - prisma → `prisma migrate dev --name <description> --create-only`.
   - rails → `bin/rails generate migration <CamelCaseDescription>`.
   - flyway → create `V<n>__<description>.sql` following project numbering.
3. Populate `up` from `up_sql_or_ops`. Populate `down` from `down_sql_or_ops`. Both must be present and symmetric.
4. For destructive ops (DROP, ALTER TYPE narrow, NOT NULL added to existing column): include an explicit safeguard comment and require human approval — never silently destructive.
5. For data backfills: do them in a separate migration after the schema change, never mix.
6. Round-trip locally: `migrate up` then `migrate down` then `migrate up` on a throwaway DB. All three must succeed.
7. Set `human_gate: true` in output. Do not run apply against shared environments.

## How to think
- Adding NOT NULL to an existing column → require backfill migration first; STOP if no backfill present.
- Renaming a column with live readers → split into add-new + dual-write + drop-old across releases; do not do it in one step.
- Autogen diff includes unrelated changes → STOP and ask human; do not commit a noisy migration.

## Required inputs
All four fields non-empty. `down_sql_or_ops` must fully undo `up_sql_or_ops`.

## Output format
{"patch": "unified diff", "touched_paths": ["migrations/2026_05_19_add_users_table.py"], "migration_path": "migrations/2026_05_19_add_users_table.py", "rationale": "1-3 sentences", "confidence": 0.0, "human_gate": true}

## Quality criteria
Passes if: file created via tool CLI with correct ordering; up/down round-trips cleanly on a throwaway DB; no data + schema mixed in one migration; destructive ops flagged.
Fails if: irreversible without explicit override; hand-authored filename with wrong sequence; autogen diff includes unrelated tables; `human_gate` not set.

## Common pitfalls
- Editing an already-applied migration. Forbidden — create a new one.
- Mixing schema and backfill. Split into two migrations.
- Adding `op.execute("UPDATE ...")` for a large table without batching. Will lock prod.

## Examples
Alembic:
```python
"""add users table"""
def upgrade():
    op.create_table("users",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("email", sa.String(255), nullable=False, unique=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
    )

def downgrade():
    op.drop_table("users")
```

Anti-pattern:
```python
def upgrade():
    op.drop_column("users", "email")              # destructive, no down
def downgrade():
    pass                                          # NOT a real reversal
```

## Stop condition
Migration file present at `migration_path`; up→down→up round-trip green on throwaway DB; `human_gate: true` emitted; no other tables modified.

## Confidence guidance
Lower when: destructive (≤0.7), data + schema mixed (≤0.6), large-table backfill (≤0.7), autogen noisy (≤0.6), tool unfamiliar (≤0.75). Floor 0.85 to proceed.
