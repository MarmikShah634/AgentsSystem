#!/usr/bin/env bash
# install-caveman.sh — one-shot installer for Caveman.
#
# Usage:
#   ./scripts/install-caveman.sh

set -euo pipefail

if command -v caveman >/dev/null 2>&1; then
  echo "[caveman] already installed: $(caveman --version 2>/dev/null || echo present)"
  exit 0
fi

case "$(uname -s)" in
  Linux*|Darwin*|MINGW*|MSYS*)
    echo "[caveman] installing via official installer"
    curl -fsSL https://raw.githubusercontent.com/JuliusBrussee/caveman/main/install.sh | bash
    ;;
  *)
    echo "[caveman] unsupported platform $(uname -s) — install manually:" >&2
    echo "  https://github.com/juliusbrussee/caveman" >&2
    exit 1
    ;;
esac

if ! command -v caveman >/dev/null 2>&1; then
  echo "[caveman] install completed but binary not on PATH — open a new shell" >&2
  exit 1
fi

# Generate rule files for tools that don't auto-activate (Cursor etc.).
caveman --with-init >/dev/null 2>&1 || true
echo "[caveman] ready. Use /caveman inside any agent session."
