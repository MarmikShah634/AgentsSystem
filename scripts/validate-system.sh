#!/usr/bin/env bash
# validate-system.sh — run all consistency checks before committing.

set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"

echo "[validate] orchestrator registry ownership check"
python3 -m orchestrator.cli validate

echo "[validate] hook scripts have shebang + are executable"
for f in hooks/*.sh; do
  head -1 "$f" | grep -q '^#!' || { echo "FAIL: $f missing shebang"; exit 1; }
done

echo "[validate] every agent referenced by at least one skill"
python3 - <<'PY'
import re, sys, pathlib
agents = {p.stem for p in pathlib.Path("agents").glob("*.md")}
owners = set()
for p in pathlib.Path("skills").glob("**/SKILL.md"):
    text = p.read_text()
    m = re.search(r"owner_agent:\s*(\S+)", text)
    if m: owners.add(m.group(1).strip().strip('"').strip("'"))
unused = agents - owners
if unused:
    print(f"WARN: agents with no skills: {sorted(unused)}")
PY

echo "[validate] all checks passed"
