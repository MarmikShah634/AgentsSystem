#!/usr/bin/env bash
# pre-task-plan.sh
# Fail closed if a task is about to run without a registered plan.
#
# Inputs (env):
#   ADS_PLAN_ID   - plan uuid the task references
#
# Exit codes:
#   0   plan exists, proceed
#   1   no ADS_PLAN_ID
#   2   plan file not found

set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

if [[ -z "${ADS_PLAN_ID:-}" ]]; then
  echo "[pre-task-plan] ADS_PLAN_ID not set — no plan, no execute." >&2
  exit 1
fi

PLAN_FILE="$ROOT/logs/plans/${ADS_PLAN_ID}.json"
if [[ ! -f "$PLAN_FILE" ]]; then
  echo "[pre-task-plan] plan file missing: $PLAN_FILE" >&2
  exit 2
fi

echo "[pre-task-plan] plan ${ADS_PLAN_ID} present — proceeding"
