#!/usr/bin/env bash
# pre-deploy-check.sh
# Refuses to deploy unless the latest security and test results are green.

set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
DATE="$(date -u +%Y-%m-%d)"
LOG="$ROOT/logs/audit/${DATE}.jsonl"

[[ -f "$LOG" ]] || { echo "[pre-deploy-check] no audit log for today" >&2; exit 1; }

# Last security-scan result must be ok
if grep -E '"skill":"security-scan"' "$LOG" | tail -1 | grep -q '"result":"ok"'; then
  echo "[pre-deploy-check] security-scan ok"
else
  echo "[pre-deploy-check] last security-scan was not ok — refusing deploy" >&2
  exit 5
fi

# Last run-tests result must be ok
if grep -E '"skill":"run-tests"' "$LOG" | tail -1 | grep -q '"result":"ok"'; then
  echo "[pre-deploy-check] run-tests ok"
else
  echo "[pre-deploy-check] last run-tests was not ok — refusing deploy" >&2
  exit 6
fi
