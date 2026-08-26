from __future__ import annotations

from dataclasses import dataclass, field


@dataclass
class TargetArchitectureIR:
    nodes: dict[str, str] = field(default_factory=dict)
    edges: list[tuple[str, str]] = field(default_factory=list)
    subgraphs: dict[str, set[str]] = field(default_factory=dict)
    sources: list[str] = field(default_factory=list)

