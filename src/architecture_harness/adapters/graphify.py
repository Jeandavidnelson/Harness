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
    if not isinstance(data, dict) or not isinstance(data.get("nodes"), list) or not isinstance(data.get("edges"), list):
        raise GraphifyError("Graphify output must contain nodes and edges arrays")

    graph = ObservedGraphIR()
    for raw in data["nodes"]:
        if not isinstance(raw, dict) or not raw.get("id"):
            raise GraphifyError("Every Graphify node requires an id")
        node = Node(str(raw["id"]), str(raw.get("kind", "unknown")), raw.get("file"))
        graph.nodes[node.id] = node
    for raw in data["edges"]:
        if not isinstance(raw, dict) or not raw.get("source") or not raw.get("target"):
            raise GraphifyError("Every Graphify edge requires source and target")
        edge = Edge(
            str(raw["source"]), str(raw["target"]), str(raw.get("relation", "depends_on")),
            str(raw.get("provenance", "EXTRACTED")).upper(), raw.get("source_file"),
        )
        graph.edges.append(edge)
        graph.nodes.setdefault(edge.source, Node(edge.source))
        graph.nodes.setdefault(edge.target, Node(edge.target))
    return graph

