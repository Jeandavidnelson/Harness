from __future__ import annotations

from collections import deque

from architecture_harness.ir.graph import Edge, ObservedGraphIR


def shortest_path(graph: ObservedGraphIR, source: str, targets: set[str]) -> list[str] | None:
    if source in targets:
        return [source]
    adjacency: dict[str, list[str]] = {}
    for edge in graph.edges:
        if edge.provenance != "AMBIGUOUS":
            adjacency.setdefault(edge.source, []).append(edge.target)
    queue = deque([(source, [source])])
    visited = {source}
    while queue:
        node, path = queue.popleft()
        for neighbor in sorted(adjacency.get(node, [])):
            if neighbor in visited:
                continue
            candidate = path + [neighbor]
            if neighbor in targets:
                return candidate
            visited.add(neighbor)
            queue.append((neighbor, candidate))
    return None


def edge_for(graph: ObservedGraphIR, source: str, target: str) -> Edge | None:
    return next((edge for edge in graph.edges if edge.source == source and edge.target == target and edge.provenance != "AMBIGUOUS"), None)

