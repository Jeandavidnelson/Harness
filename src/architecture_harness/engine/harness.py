from __future__ import annotations

from dataclasses import dataclass

from architecture_harness.engine.matcher import resolve
from architecture_harness.engine.paths import edge_for, shortest_path
from architecture_harness.engine.violations import Violation
from architecture_harness.ir.architecture import TargetArchitectureIR
from architecture_harness.ir.graph import ObservedGraphIR
from architecture_harness.ir.rules import Rule, RulesIR


@dataclass
class HarnessResult:
    violations: list[Violation]

    @property
    def status(self) -> str:
        if any(violation.blocking for violation in self.violations):
            return "FAIL"
        return "WARN" if self.violations else "PASS"


def _evidence(graph: ObservedGraphIR, path: list[str]) -> tuple[tuple[str, ...], tuple[str, ...]]:
    files: list[str] = []
    provenance: list[str] = []
    for node in path:
        file = graph.nodes[node].file
        if file and file not in files:
            files.append(file)
    for source, target in zip(path, path[1:]):
        edge = edge_for(graph, source, target)
        if edge:
            if edge.source_file and edge.source_file not in files:
                files.append(edge.source_file)
            if edge.provenance not in provenance:
                provenance.append(edge.provenance)
    return tuple(files), tuple(provenance)


def _violation(rule: Rule, graph: ObservedGraphIR, path: list[str], target: str | None = None) -> Violation:
    files, provenance = _evidence(graph, path)
    expected = f"{rule.source} {rule.type} {rule.target}"
    return Violation(
        rule.id, rule.type, path[0], target or path[-1], tuple(path), files, provenance,
        rule.severity, rule.status, rule.rationale, expected,
    )


def evaluate(observed: ObservedGraphIR, target: TargetArchitectureIR, rules: RulesIR) -> HarnessResult:
    violations: list[Violation] = []
    for rule in rules.rules:
        sources = resolve(rule.source, observed, target, rules)
        targets = resolve(rule.target, observed, target, rules)
        allowed: set[str] = set()
        for reference in rule.allowed_targets:
            allowed.update(resolve(reference, observed, target, rules) or {reference})
        effective_targets = targets - allowed

        if rule.type == "forbidden_edge":
            for edge in observed.edges:
                if edge.provenance != "AMBIGUOUS" and edge.source in sources and edge.target in effective_targets:
                    violations.append(_violation(rule, observed, [edge.source, edge.target]))
        elif rule.type == "required_edge":
            for source in sorted(sources):
                if not any(edge_for(observed, source, target_node) for target_node in targets):
                    violations.append(_violation(rule, observed, [source], rule.target))
        elif rule.type == "forbidden_path":
            for source in sorted(sources):
                path = shortest_path(observed, source, effective_targets)
                if path:
                    violations.append(_violation(rule, observed, path))
        elif rule.type == "required_path":
            for source in sorted(sources):
                path = shortest_path(observed, source, targets)
                if not path:
                    violations.append(_violation(rule, observed, [source], rule.target))
    return HarnessResult(violations)
