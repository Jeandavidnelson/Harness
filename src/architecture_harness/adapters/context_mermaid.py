from __future__ import annotations

from pathlib import Path

from architecture_harness.adapters.mermaid import MermaidError, parse_mermaid
from architecture_harness.ir.context import ContextGraphIR
from architecture_harness.ir.graph import Edge, Node


def load_context_directory(directory: str | Path) -> ContextGraphIR:
    files = sorted(Path(directory).glob("*.mmd"))
    if not files:
        raise MermaidError(f"No context Mermaid files found in {directory}")
    result = ContextGraphIR()
    for path in files:
        parsed = parse_mermaid(path.read_text(encoding="utf-8"), str(path))
        for identifier in parsed.nodes:
            result.nodes.setdefault(identifier, Node(identifier, "declared_context"))
        result.edges.extend(
            Edge(source, target, "declared_relation", "DECLARED_CONTEXT", str(path))
            for source, target in parsed.edges
        )
    return result

