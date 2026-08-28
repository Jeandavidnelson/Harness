from __future__ import annotations

from architecture_harness.engine.matcher import resolve
from architecture_harness.ir.architecture import TargetArchitectureIR
from architecture_harness.ir.context import CompactTaskContext, ContextGraphIR
from architecture_harness.ir.graph import Edge, ObservedGraphIR
from architecture_harness.ir.rules import RulesIR


def _expand(seeds: set[str], edges: list[Edge], radius: int, limit: int) -> tuple[set[str], bool]:
    selected = set(seeds)
    frontier = set(seeds)
    truncated = False
    for _ in range(radius):
        candidates = sorted({
            endpoint
            for edge in edges
            if edge.source in frontier or edge.target in frontier
            for endpoint in (edge.source, edge.target)
        } - selected)
        room = max(0, limit - len(selected))
        if len(candidates) > room:
            truncated = True
        new = set(candidates[:room])
        if not new:
            break
        selected.update(new)
        frontier = new
    return selected, truncated


def select_context(
    focus: list[str], observed: ObservedGraphIR, context: ContextGraphIR,
    target: TargetArchitectureIR, rules: RulesIR, radius: int = 1, max_items: int = 50,
) -> CompactTaskContext:
    if radius < 0 or max_items < 1:
        raise ValueError("radius must be >= 0 and max-items must be >= 1")
    seeds = {identifier for term in focus for identifier in observed.nodes if term.lower() in identifier.lower()}
    seeds.update(term for term in focus if term in context.nodes)
    if not seeds:
        raise ValueError("No focus node matches the observed or declared graphs")
    observed_nodes, truncated = _expand(seeds & observed.nodes.keys(), observed.edges, radius, max_items)
    context_seeds = (seeds | observed_nodes) & context.nodes.keys()
    context_nodes, context_truncated = _expand(context_seeds, context.edges, radius + 1, max_items)
    selected = observed_nodes | context_nodes
    observed_edges = [e for e in observed.edges if e.source in observed_nodes and e.target in observed_nodes][:max_items]
    context_edges = [e for e in context.edges if e.source in context_nodes and e.target in context_nodes][:max_items]
    target_edges = []
    for edge in target.edges:
        logical_nodes = resolve(edge[0], observed, target, rules) | resolve(edge[1], observed, target, rules)
        if logical_nodes & observed_nodes:
            target_edges.append(edge)
    target_edges = target_edges[:max_items]
    applicable: list[str] = []
    for rule in rules.rules:
        endpoints = resolve(rule.source, observed, target, rules) | resolve(rule.target, observed, target, rules)
        if endpoints & observed_nodes:
            detail = f"{rule.id} [{rule.severity}/{rule.status}]: {rule.type} {rule.source} -> {rule.target}"
            if rule.rationale:
                detail += f"; rationale={rule.rationale}"
            applicable.append(detail)
    files = sorted({observed.nodes[node].file for node in observed_nodes if observed.nodes[node].file})
    edge_truncated = any(len(items) >= max_items for items in (observed_edges, context_edges, target_edges))
    return CompactTaskContext(tuple(focus), observed_edges, context_edges, target_edges, applicable[:max_items], files[:max_items], truncated or context_truncated or edge_truncated)
