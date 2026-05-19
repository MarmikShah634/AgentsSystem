#!/usr/bin/env bash
# new-skill.sh — scaffold a new single-task skill.
#
# Usage:
#   ./scripts/new-skill.sh <category> <skill-id> <owner-agent>

set -euo pipefail

CAT="${1:?category required (e.g. coding)}"
ID="${2:?skill id required}"
OWNER="${3:?owner agent required}"

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
DIR="$ROOT/skills/$CAT/$ID"

if [[ -d "$DIR" ]]; then
  echo "skill already exists: $DIR" >&2
  exit 1
fi

mkdir -p "$DIR"
cat > "$DIR/SKILL.md" <<EOF
---
id: $ID
category: $CAT
owner_agent: $OWNER
inputs: []
outputs: []
requires_plan: true
emits_confidence: true
---

# Skill: $ID

## Task

<one sentence describing the single task this skill performs>

## Stop condition

<observable condition that ends the skill>
EOF

echo "created $DIR/SKILL.md"
