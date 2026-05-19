#!/usr/bin/env bash
# post-task-log.sh
# Append a task-completion record to logs/audit/<date>.jsonl.
#
# Inputs (env):
#   ADS_PLAN_ID, ADS_STEP_ID, ADS_AGENT, ADS_SKILL,
#   ADS_CONFIDENCE, ADS_RESULT, ADS_DURATION_MS

set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
DATE="$(date -u +%Y-%m-%d)"
TS="$(date -u +%Y-%m-%dT%H:%M:%SZ)"

mkdir -p "$ROOT/logs/audit"
LOG="$ROOT/logs/audit/${DATE}.jsonl"

cat >>"$LOG" <<EOF
{"ts":"$TS","plan_id":"${ADS_PLAN_ID:-}","step_id":"${ADS_STEP_ID:-}","agent":"${ADS_AGENT:-}","skill":"${ADS_SKILL:-}","confidence":${ADS_CONFIDENCE:-0.0},"result":"${ADS_RESULT:-unknown}","duration_ms":${ADS_DURATION_MS:-0}}
EOF
