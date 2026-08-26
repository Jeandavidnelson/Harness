from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(frozen=True)
class Node:
    id: str
    kind: str = "unknown"
    file: str | None = None


@dataclass(frozen=True)
class Edge:
    source: str
    target: str
    relation: str = "depends_on"
    provenance: str = "EXTRACTED"
    source_file: str | None = None


@dataclass
class ObservedGraphIR:
    nodes: dict[str, Node] = field(default_factory=dict)
    edges: list[Edge] = field(default_factory=list)

    def summary(self) -> dict[str, int]:
        result = {"nodes": len(self.nodes), "edges": len(self.edges)}
        for provenance in ("EXTRACTED", "INFERRED", "AMBIGUOUS"):
            result[provenance.lower()] = sum(
                edge.provenance.upper() == provenance for edge in self.edges
            )
        return result

