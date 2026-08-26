#!/bin/sh
set -eu

SCRIPT_DIR=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
PROJECT_ROOT=$(dirname "$SCRIPT_DIR")

if command -v graphify >/dev/null 2>&1; then
  graphify --output "$PROJECT_ROOT/graphify-out/graph.json" "$PROJECT_ROOT"
else
  echo "Graphify executable unavailable; validating the trusted existing output."
  "$PROJECT_ROOT/.venv/bin/arch-harness" --root "$PROJECT_ROOT" observed
fi

