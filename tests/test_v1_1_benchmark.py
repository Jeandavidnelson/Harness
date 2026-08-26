from pathlib import Path

from architecture_harness.config import ProjectPaths
from architecture_harness.metrics.v1_1_benchmark import run_v1_1_benchmark


def test_real_graphify_vs_agent_context_benchmark():
    root = Path(__file__).parents[1]
    rows = run_v1_1_benchmark(ProjectPaths(root), root / "experiments" / "tasks.yaml", task_limit=1)
    assert [row.condition for row in rows] == ["A_GRAPHIFY", "B_GRAPHIFY_FULL_ARCH", "C_AGENT_CONTEXT"]
    assert rows[2].context_tokens < rows[1].context_tokens
    assert rows[2].harness_result == "PASS"
    assert rows[0].task_success == "NOT_MEASURED"

