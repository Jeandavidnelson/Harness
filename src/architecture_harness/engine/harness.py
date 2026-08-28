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
    assessments: list["RuleAssessment"] | None = None

    def __post_init__(self) -> None:
        if self.assessments is None:
            self.assessments = []

    @property
    def status(self) -> str:
        if any(violation.blocking for violation in self.violations):
            return "FAIL"
        if any(item.status == "UNRESOLVED" for item in self.assessments or []):
            return "UNRESOLVED"
        if self.assessments and all(item.status == "NOT_APPLICABLE" for item in self.assessments):
            return "NOT_APPLICABLE"
        return "WARN" if self.violations else "PASS"

    @property
    def exit_code(self) -> int:
        if self.status == "FAIL":
            return 1
        if self.status == "UNRESOLVED":
            return 2
        return 0


@dataclass(frozen=True)
class RuleAssessment:
    rule_id: str
    status: str
    reason: str
    source_matches: tuple[str, ...] = ()
    target_matches: tuple[str, ...] = ()

    def to_dict(self) -> dict[str, object]:
        return {
            "rule_id": self.rule_id,
            "status": self.status,
            "reason": self.reason,
            "source_matches": list(self.source_matches),
            "target_matches": list(self.target_matches),
        }


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
    assessments: list[RuleAssessment] = []
    for rule in rules.rules:
        sources = resolve(rule.source, observed, target, rules)
        targets = resolve(rule.target, observed, target, rules)
        if rule.applicability == "declared_only":
            assessments.append(RuleAssessment(
                rule.id, "NOT_APPLICABLE", "Rule is declared guidance and is not evaluated against observed code.",
                tuple(sorted(sources)), tuple(sorted(targets)),
            ))
            continue
        if not sources or not targets:
            missing = ", ".join(name for name, matches in (("source", sources), ("target", targets)) if not matches)
            status = "UNRESOLVED" if rule.applicability == "required" and rule.status == "validated" else "NOT_APPLICABLE"
            reason = (
                f"Required validated rule cannot resolve its {missing} mapping."
                if status == "UNRESOLVED"
                else f"Rule applies when observed; its {missing} mapping is not present in the observed graph."
            )
            assessments.append(RuleAssessment(rule.id, status, reason, tuple(sorted(sources)), tuple(sorted(targets))))
            continue
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
        assessments.append(RuleAssessment(
            rule.id,
            "FAIL" if any(item.rule_id == rule.id for item in violations) else "PASS",
            "Blocking or advisory violation detected." if any(item.rule_id == rule.id for item in violations) else "Rule evaluated against observed source and target mappings.",
            tuple(sorted(sources)), tuple(sorted(targets)),
        ))
    return HarnessResult(violations, assessments)
