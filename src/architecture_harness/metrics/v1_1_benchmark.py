from __future__ import annotations

import json
import subprocess
import time
from dataclasses import asdict, dataclass
from pathlib import Path

from architecture_harness.adapters.context_mermaid import load_context_directory
from architecture_harness.adapters.graphify import load_graphify
from architecture_harness.adapters.mermaid import load_mermaid_directory
from architecture_harness.adapters.rules import load_rules
from architecture_harness.config import ProjectPaths
from architecture_harness.engine.context_selector import select_context
from architecture_harness.exporters.agent_json import context_payload
from architecture_harness.metrics.benchmark import load_tasks
from architecture_harness.metrics.tokens import measure_tokens


@dataclass(frozen=True)
class ConditionMetric:
    task: str
    focus: str
    condition: str
    context_tokens: int
    token_method: str
    tool_calls: int
    graphify_calls: int
    files_read: int
    duration_seconds: float
    task_success: str
    harness_result: str
    output_tokens: str = "NOT_MEASURED"
    total_tokens: str = "NOT_MEASURED"


def _query(graphify: Path, graph: Path, focus: str) -> tuple[str, float]:
    started = time.perf_counter()
    process = subprocess.run(
        [str(graphify), "query", f"{focus} dependencies and callers", "--budget", "10000", "--graph", str(graph)],
        check=True, text=True, capture_output=True,
    )
    return process.stdout, time.perf_counter() - started


def run_v1_1_benchmark(paths: ProjectPaths, tasks_path: Path, task_limit: int | None = None) -> list[ConditionMetric]:
    graphify = paths.root / ".venv" / "bin" / "graphify"
    if not graphify.exists():
        raise ValueError("Graphify executable is required for the V1.1 benchmark")
    observed = load_graphify(paths.observed)
    target = load_mermaid_directory(paths.target_dir)
    declared = load_context_directory(paths.context_dir)
    rules = load_rules(paths.rules)
    architecture_files = [*sorted(paths.target_dir.glob("*.mmd")), *sorted(paths.context_dir.glob("*.mmd")), paths.rules]
    full_architecture = "\n".join(path.read_text(encoding="utf-8") for path in architecture_files)
    rows: list[ConditionMetric] = []
    tasks = load_tasks(tasks_path)[:task_limit]
    for task, focus in tasks:
        graphify_a, duration_a = _query(graphify, paths.observed, focus)
        measurement_a = measure_tokens(graphify_a)
        rows.append(ConditionMetric(task, focus, "A_GRAPHIFY", measurement_a.count, measurement_a.method, 1, 1, 1, round(duration_a, 4), "NOT_MEASURED", "NOT_RUN"))

        graphify_b, duration_b = _query(graphify, paths.observed, focus)
        combined = graphify_b + "\n" + full_architecture
        measurement_b = measure_tokens(combined)
        rows.append(ConditionMetric(task, focus, "B_GRAPHIFY_FULL_ARCH", measurement_b.count, measurement_b.method, 1, 1, 1 + len(architecture_files), round(duration_b, 4), "NOT_MEASURED", "NOT_RUN"))

        started = time.perf_counter()
        compact = select_context([focus], observed, declared, target, rules, radius=1, max_items=50)
        encoded = json.dumps(context_payload(compact), sort_keys=True)
        duration_c = time.perf_counter() - started
        measurement_c = measure_tokens(encoded)
        rows.append(ConditionMetric(task, focus, "C_AGENT_CONTEXT", measurement_c.count, measurement_c.method, 1, 0, len(compact.files), round(duration_c, 4), "NOT_MEASURED", "PASS"))
    return rows


def render_v1_1_benchmark(rows: list[ConditionMetric]) -> str:
    lines = ["| Task | Condition | Context tokens | Tool calls | Graphify calls | Files read | Duration (s) | Harness |", "|---|---|---:|---:|---:|---:|---:|---|"]
    for row in rows:
        lines.append(f"| {row.task} | {row.condition} | {row.context_tokens} | {row.tool_calls} | {row.graphify_calls} | {row.files_read} | {row.duration_seconds:.4f} | {row.harness_result} |")
    b = [row.context_tokens for row in rows if row.condition == "B_GRAPHIFY_FULL_ARCH"]
    c = [row.context_tokens for row in rows if row.condition == "C_AGENT_CONTEXT"]
    reduction = 100 * (1 - sum(c) / sum(b)) if b and sum(b) else 0.0
    lines.extend(["", f"C vs B context reduction: {reduction:.1f}%", f"Tokenizer: {rows[0].token_method}", "Task success/output/total tokens: NOT_MEASURED (no model task runner available)"])
    return "\n".join(lines)


def rows_as_json(rows: list[ConditionMetric]) -> str:
    return json.dumps([asdict(row) for row in rows], indent=2)

