#!/bin/sh
set -eu

SCRIPT_DIR=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
PROJECT_ROOT=$(dirname "$SCRIPT_DIR")
CLI="$PROJECT_ROOT/.venv/bin/arch-harness"
PYTHON="$PROJECT_ROOT/.venv/bin/python"
PYTEST="$PROJECT_ROOT/.venv/bin/pytest"
SKILL_VALIDATOR="/Users/jean-david/.codex/skills/.system/skill-creator/scripts/quick_validate.py"

"$SCRIPT_DIR/refresh_graph.sh"
"$CLI" --root "$PROJECT_ROOT" stale
"$CLI" --root "$PROJECT_ROOT" agent doctor --format json
"$PYTEST" -q "$PROJECT_ROOT/tests"
"$CLI" --root "$PROJECT_ROOT" check
BENCHMARK=$($CLI --root "$PROJECT_ROOT" benchmark --mode v1.1)
echo "$BENCHMARK"
"$PYTEST" -q "$PROJECT_ROOT/tests/test_ace_author.py"
"$PYTHON" "$SKILL_VALIDATOR" "$PROJECT_ROOT/integrations/ace-rule-author"

{
  echo ""
  echo "## Validation automatisée V1.1 — $(date +%Y-%m-%dT%H:%M:%S%z)"
  echo ""
  echo "- Graphify refresh and stale check: PASS"
  echo "- doctor / pytest / harness: PASS"
  echo "- ACE tests and skill validation: PASS"
  echo ""
  echo "$BENCHMARK"
} >> "$PROJECT_ROOT/logs/V1_1_IMPLEMENTATION_LOG.md"

