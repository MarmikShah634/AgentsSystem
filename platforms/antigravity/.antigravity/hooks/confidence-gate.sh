#!/usr/bin/env bash
# confidence-gate.sh
# Reads a confidence score from $ADS_CONFIDENCE and blocks if below floor.
#
# Inputs (env):
#   ADS_CONFIDENCE   - float in [0,1]
#   ADS_FLOOR        - optional float, default 0.90
#
# Exit codes:
#   0  pass
#   3  below floor (caller should prompt human)

set -euo pipefail

FLOOR="${ADS_FLOOR:-0.90}"
CONF="${ADS_CONFIDENCE:-0.0}"

awk -v c="$CONF" -v f="$FLOOR" 'BEGIN { exit !(c+0 >= f+0) }' || {
  echo "[confidence-gate] confidence=$CONF below floor=$FLOOR" >&2
  exit 3
}

echo "[confidence-gate] confidence=$CONF >= floor=$FLOOR"
