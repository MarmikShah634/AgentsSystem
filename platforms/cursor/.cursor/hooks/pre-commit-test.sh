#!/usr/bin/env bash
# pre-commit-test.sh
# Runs the project's native test command before allowing a commit.
# Detects the test command via the stack signal files.

set -euo pipefail

if   [[ -f package.json   ]]; then CMD="${ADS_TEST_CMD:-npm test --silent}"
elif [[ -f pyproject.toml ]]; then CMD="${ADS_TEST_CMD:-pytest -q}"
elif [[ -f go.mod         ]]; then CMD="${ADS_TEST_CMD:-go test ./...}"
elif [[ -f Cargo.toml     ]]; then CMD="${ADS_TEST_CMD:-cargo test}"
elif [[ -f Gemfile        ]]; then CMD="${ADS_TEST_CMD:-bundle exec rspec}"
else
  echo "[pre-commit-test] unknown stack — skipping (set ADS_TEST_CMD to override)"
  exit 0
fi

echo "[pre-commit-test] running: $CMD"
eval "$CMD"
