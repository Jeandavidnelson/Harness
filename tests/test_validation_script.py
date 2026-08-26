from pathlib import Path


def test_v1_1_validation_order_and_fail_fast():
    script = (Path(__file__).parents[1] / "scripts" / "validate_v1_1.sh").read_text()
    assert "set -eu" in script
    ordered = [
        '"$SCRIPT_DIR/refresh_graph.sh"',
        '"$CLI" --root "$PROJECT_ROOT" stale',
        '"$CLI" --root "$PROJECT_ROOT" agent doctor',
        '"$PYTEST" -q "$PROJECT_ROOT/tests"',
        '"$CLI" --root "$PROJECT_ROOT" check',
        'benchmark --mode v1.1',
        '"$PYTEST" -q "$PROJECT_ROOT/tests/test_ace_author.py"',
        '"$PYTHON" "$SKILL_VALIDATOR"',
    ]
    positions = [script.index(term) for term in ordered]
    assert positions == sorted(positions)
