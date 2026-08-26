from __future__ import annotations

from dataclasses import dataclass, field

from architecture_harness.ir.graph import Edge, Node


@dataclass
class ContextGraphIR:
    nodes: dict[str, Node] = field(default_factory=dict)
    edges: list[Edge] = field(default_factory=list)


@dataclass
class CompactTaskContext:
    focus: tuple[str, ...]
    observed_edges: list[Edge]
    context_edges: list[Edge]
    target_edges: list[tuple[str, str]]
    applicable_rules: list[str]
    files: list[str]
    truncated: bool = False

