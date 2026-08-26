#!/bin/sh
set -eu

SCRIPT_DIR=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
PROJECT_ROOT=$(dirname "$SCRIPT_DIR")
CLI="$PROJECT_ROOT/.venv/bin/arch-harness"

"$SCRIPT_DIR/refresh_graph.sh"
"$CLI" --root "$PROJECT_ROOT" target
"$CLI" --root "$PROJECT_ROOT" rules validate
"$PROJECT_ROOT/.venv/bin/pytest" -q "$PROJECT_ROOT/tests"
"$CLI" --root "$PROJECT_ROOT" check
BENCHMARK=$($CLI --root "$PROJECT_ROOT" benchmark)
echo "$BENCHMARK"
{
  echo ""
  echo "## Validation automatisée — $(date +%Y-%m-%dT%H:%M:%S%z)"
  echo ""
  echo "- refresh Graphify: PASS (trusted existing output when executable unavailable)"
  echo "- Mermaid/rules/tests/harness: PASS"
  echo ""
  echo "$BENCHMARK"
} >> "$PROJECT_ROOT/logs/V1_IMPLEMENTATION_LOG.md"

