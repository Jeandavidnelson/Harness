from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from architecture_harness.ir.graph import Edge, Node, ObservedGraphIR


class GraphifyError(ValueError):
    pass


def load_graphify(path: str | Path) -> ObservedGraphIR:
    source = Path(path)
    try:
        data: Any = json.loads(source.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise GraphifyError(f"Cannot read Graphify output {source}: {exc}") from exc
    edge_data = data.get("edges") if isinstance(data, dict) else None
    if edge_data is None and isinstance(data, dict):
        edge_data = data.get("links")
    if not isinstance(data, dict) or not isinstance(data.get("nodes"), list) or not isinstance(edge_data, list):
        raise GraphifyError("Graphify output must contain nodes and edges/links arrays")

    graph = ObservedGraphIR()
    for raw in data["nodes"]:
        if not isinstance(raw, dict) or not raw.get("id"):
            raise GraphifyError("Every Graphify node requires an id")
        node = Node(
            str(raw["id"]),
            str(raw.get("kind", raw.get("type", raw.get("file_type", "unknown")))),
            raw.get("file") or raw.get("source_file"),
        )
        graph.nodes[node.id] = node
    for raw in edge_data:
        if not isinstance(raw, dict) or not raw.get("source") or not raw.get("target"):
            raise GraphifyError("Every Graphify edge requires source and target")
        edge = Edge(
            str(raw["source"]), str(raw["target"]), str(raw.get("relation", "depends_on")),
            str(raw.get("provenance", raw.get("confidence", "EXTRACTED"))).upper(), raw.get("source_file"),
        )
        graph.edges.append(edge)
        graph.nodes.setdefault(edge.source, Node(edge.source))
        graph.nodes.setdefault(edge.target, Node(edge.target))
    return graph
