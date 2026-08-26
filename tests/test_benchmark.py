from pathlib import Path

from architecture_harness.config import ProjectPaths
from architecture_harness.metrics.benchmark import run_benchmark


def test_compact_context_is_smaller_than_baseline():
    root = Path(__file__).parents[1]
    rows = run_benchmark(ProjectPaths(root), root / "experiments" / "tasks.yaml")
    assert len(rows) == 5
    assert all(row.v1_context_tokens < row.raw_context_tokens for row in rows)

