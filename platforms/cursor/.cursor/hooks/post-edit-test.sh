#!/usr/bin/env bash
# post-edit-test.sh
# After a code edit, ensure a paired test file exists. If not, exit non-zero
# so the orchestrator schedules a generate-unit-test or generate-puppeteer-test
# step before the next edit.
#
# Inputs (env):
#   ADS_EDITED_PATH  - path of the file just edited

set -euo pipefail

EDITED="${ADS_EDITED_PATH:-}"
[[ -n "$EDITED" ]] || { echo "[post-edit-test] no ADS_EDITED_PATH" >&2; exit 1; }

# Heuristics for "is this a code file that needs a test"
case "$EDITED" in
  *test*|*spec*|*_test.*|*.test.*|*.spec.*) echo "[post-edit-test] $EDITED is itself a test — ok"; exit 0;;
  *.md|*.txt|*.json|*.yaml|*.yml|*.toml|*.lock) echo "[post-edit-test] $EDITED is non-code — ok"; exit 0;;
esac

base="$(basename "$EDITED")"
stem="${base%.*}"
ext="${base##*.}"

# Look for *any* file in the repo that references this path or its stem
# inside a test directory.
if grep -rln --include='*test*' --include='*spec*' -e "$stem" -e "$EDITED" \
       . 2>/dev/null | grep -q .; then
  echo "[post-edit-test] paired test reference found for $EDITED"
  exit 0
fi

echo "[post-edit-test] no paired test for $EDITED — scheduling test gen" >&2
exit 4
