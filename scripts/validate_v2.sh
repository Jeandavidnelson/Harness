#!/bin/sh
set -eu

SCRIPT_DIR=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
PROJECT_ROOT=$(dirname "$SCRIPT_DIR")
CLI="$PROJECT_ROOT/.venv/bin/arch-harness"
PYTHON="$PROJECT_ROOT/.venv/bin/python"
PYTEST="$PROJECT_ROOT/.venv/bin/pytest"
SKILL_VALIDATOR="${CODEX_HOME:-$HOME/.codex}/skills/.system/skill-creator/scripts/quick_validate.py"

cd "$PROJECT_ROOT"

"$SCRIPT_DIR/refresh_graph.sh"
"$CLI" --root "$PROJECT_ROOT" stale
"$CLI" --root "$PROJECT_ROOT" doctor
"$PYTEST" -q "$PROJECT_ROOT/tests"
"$CLI" --root "$PROJECT_ROOT" gate --format json
"$CLI" --root "$PROJECT_ROOT" capabilities --format json
"$CLI" --root "$PROJECT_ROOT" benchmark --mode v2
"$PYTHON" "$PROJECT_ROOT/experiments/run_v2_test_lab.py"
"$PYTHON" "$SKILL_VALIDATOR" "$PROJECT_ROOT/skills/architecture-rule-author"
"$PYTHON" "$SKILL_VALIDATOR" "$PROJECT_ROOT/integrations/archunit"
"$PYTHON" - <<'PY'
import tomllib
from pathlib import Path
for path in Path("integrations/bmad/overrides").glob("*.toml"):
    tomllib.loads(path.read_text(encoding="utf-8"))
print("BMAD overrides: valid")
PY

echo "Architecture Harness V2 validation: PASS"
