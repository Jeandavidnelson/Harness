from copy import deepcopy
from pathlib import Path

import pytest

from architecture_harness.adapters.graphify import load_graphify
from architecture_harness.adapters.mermaid import load_mermaid_directory
from architecture_harness.adapters.rules import load_rules
from architecture_harness.engine.harness import evaluate
from architecture_harness.engine.matcher import resolve
from architecture_harness.ir.graph import Edge


ROOT = Path(__file__).parents[1]


def production_inputs():
    return (
        load_graphify(ROOT / "graphify-out" / "graph.json"),
        load_mermaid_directory(ROOT / "architecture" / "diagrams"),
        load_rules(ROOT / "architecture" / "rules" / "rules.yaml"),
    )


def test_real_repository_rules_pass():
    observed, target, rules = production_inputs()
    assert len(rules.rules) == 8
    assert evaluate(observed, target, rules).status == "PASS"


@pytest.mark.parametrize("rule_id", [
    "cli-must-load-observed-graph",
    "cli-must-run-harness",
    "harness-must-resolve-explicit-roles",
    "harness-must-support-path-evidence",
    "doctor-must-validate-rules",
    "graphify-adapter-must-not-depend-on-cli",
    "token-metrics-must-not-depend-on-cli",
    "cache-must-not-call-cli",
])
def test_each_real_rule_detects_its_regression(rule_id):
    observed, target, rules = production_inputs()
    rule = next(rule for rule in rules.rules if rule.id == rule_id)
    sources = resolve(rule.source, observed, target, rules)
    targets = resolve(rule.target, observed, target, rules)
    assert len(sources) == len(targets) == 1
    source, target_node = next(iter(sources)), next(iter(targets))
    mutated = deepcopy(observed)
    if rule.type.startswith("required"):
        mutated.edges = [edge for edge in mutated.edges if edge.source != source]
    else:
        mutated.edges.append(Edge(source, target_node, relation="calls", provenance="EXTRACTED", source_file="synthetic-regression.py"))
    result = evaluate(mutated, target, rules)
    assert rule_id in {violation.rule_id for violation in result.violations}

