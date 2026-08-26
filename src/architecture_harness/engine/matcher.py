from __future__ import annotations

from architecture_harness.ir.architecture import TargetArchitectureIR
from architecture_harness.ir.graph import ObservedGraphIR
from architecture_harness.ir.rules import MatchSpec, RulesIR


def matches(identifier: str, spec: MatchSpec) -> bool:
    return all((
        spec.exact is None or identifier == spec.exact,
        spec.suffix is None or identifier.endswith(spec.suffix),
        spec.prefix is None or identifier.startswith(spec.prefix),
        spec.contains is None or spec.contains in identifier,
    ))


def resolve(reference: str, observed: ObservedGraphIR, target: TargetArchitectureIR, rules: RulesIR) -> set[str]:
    if reference in observed.nodes:
        return {reference}
    if reference in rules.roles:
        return {identifier for identifier in observed.nodes if matches(identifier, rules.roles[reference])}
    if reference in target.subgraphs:
        members = target.subgraphs[reference]
        result: set[str] = set()
        for member in members:
            result.update(resolve(member, observed, target, rules))
        return result
    return set()

