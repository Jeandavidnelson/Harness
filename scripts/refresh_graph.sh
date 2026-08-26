#!/bin/sh
set -eu

SCRIPT_DIR=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
PROJECT_ROOT=$(dirname "$SCRIPT_DIR")

GRAPHIFY="$PROJECT_ROOT/.venv/bin/graphify"
if [ ! -x "$GRAPHIFY" ]; then
  echo "Graphify is required. Install development dependencies with: .venv/bin/pip install -e '.[dev]'" >&2
  exit 2
fi

if [ -f "$PROJECT_ROOT/graphify-out/manifest.json" ]; then
  "$GRAPHIFY" update "$PROJECT_ROOT" --no-cluster
else
  "$GRAPHIFY" extract "$PROJECT_ROOT" --code-only --no-cluster
fi
"$PROJECT_ROOT/.venv/bin/arch-harness" --root "$PROJECT_ROOT" stale
"$PROJECT_ROOT/.venv/bin/arch-harness" --root "$PROJECT_ROOT" observed
