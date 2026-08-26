from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path

from architecture_harness.adapters.context_mermaid import load_context_directory
from architecture_harness.adapters.graphify import load_graphify
from architecture_harness.adapters.mermaid import load_mermaid_directory
from architecture_harness.adapters.rules import load_rules
from architecture_harness.config import ProjectPaths
from architecture_harness.engine.context_selector import select_context
from architecture_harness.exporters.llm_context import render_llm_context
from architecture_harness.metrics.tokens import measure_tokens
from architecture_harness.cache.manager import CacheManager


@dataclass(frozen=True)
class BenchmarkRow:
    task: str
    focus: str
    raw_context_tokens: int
    graphify_query_tokens: int
    v1_context_tokens: int
    reduction_percent: float
    method: str


def load_tasks(path: Path) -> list[tuple[str, str]]:
    tasks: list[tuple[str, str]] = []
    current_id = ""
    for raw in path.read_text(encoding="utf-8").splitlines():
        line = raw.strip()
        if line.startswith("- id:"):
            current_id = line.split(":", 1)[1].strip()
        elif line.startswith("focus:") and current_id:
            tasks.append((current_id, line.split(":", 1)[1].strip()))
            current_id = ""
    if not tasks:
        raise ValueError("Benchmark tasks file contains no id/focus pairs")
    return tasks


def run_benchmark(paths: ProjectPaths, tasks_path: Path, radius: int = 1, max_items: int = 30) -> list[BenchmarkRow]:
    input_paths = [paths.observed, *sorted(paths.target_dir.glob("*.mmd")), *sorted(paths.context_dir.glob("*.mmd")), paths.rules, tasks_path]
    cache = CacheManager(paths.root / ".cache" / "architecture-harness")
    cached = cache.get("benchmark", input_paths)
    if cached is not None:
        return [BenchmarkRow(**row) for row in cached]
    observed = load_graphify(paths.observed)
    target = load_mermaid_directory(paths.target_dir)
    context = load_context_directory(paths.context_dir)
    rules = load_rules(paths.rules)
    all_inputs = [paths.observed, *sorted(paths.target_dir.glob("*.mmd")), *sorted(paths.context_dir.glob("*.mmd")), paths.rules]
    raw = "\n".join(path.read_text(encoding="utf-8") for path in all_inputs)
    graph_query = json.dumps({
        "nodes": sorted(observed.nodes),
        "edges": [(e.source, e.target, e.relation, e.provenance) for e in observed.edges],
        "target": target.edges,
        "rules": [rule.__dict__ for rule in rules.rules],
    }, default=list)
    raw_measure = measure_tokens(raw)
    query_measure = measure_tokens(graph_query)
    rows: list[BenchmarkRow] = []
    for task, focus in load_tasks(tasks_path):
        compact = render_llm_context(select_context([focus], observed, context, target, rules, radius, max_items))
        compact_measure = measure_tokens(compact)
        reduction = 100 * (1 - compact_measure.count / raw_measure.count) if raw_measure.count else 0.0
        rows.append(BenchmarkRow(task, focus, raw_measure.count, query_measure.count, compact_measure.count, round(reduction, 1), compact_measure.method))
    cache.put("benchmark", input_paths, [row.__dict__ for row in rows])
    return rows


def render_benchmark(rows: list[BenchmarkRow]) -> str:
    lines = ["| Task | Focus | Raw | Graph query | V1 | Reduction |", "|---|---|---:|---:|---:|---:|"]
    for row in rows:
        lines.append(f"| {row.task} | {row.focus} | {row.raw_context_tokens} | {row.graphify_query_tokens} | {row.v1_context_tokens} | {row.reduction_percent:.1f}% |")
    average = sum(row.reduction_percent for row in rows) / len(rows)
    lines.extend(["", f"Average reduction: {average:.1f}%", f"Token method: {rows[0].method}"])
    return "\n".join(lines)
