import json
from copy import deepcopy
from pathlib import Path

import pytest

from architecture_harness.adapters.graphify import load_graphify
from architecture_harness.adapters.mermaid import load_mermaid_directory
from architecture_harness.adapters.rules import load_rules
from architecture_harness.engine.harness import evaluate
from architecture_harness.engine.matcher import resolve
from architecture_harness.exporters.json import render_json
from architecture_harness.ir.graph import Edge, Node
from architecture_harness.metrics.tokens import measure_tokens


ROOT = Path(__file__).parents[1]


@pytest.mark.parametrize("rule_id,mutation", [
    ("cli-must-run-harness", "remove_required"),
    ("graphify-adapter-must-not-depend-on-cli", "add_direct"),
    ("token-metrics-must-not-depend-on-cli", "add_indirect"),
])
def test_three_compact_production_correction_loops(rule_id, mutation):
    observed = load_graphify(ROOT / "graphify-out" / "graph.json")
    target = load_mermaid_directory(ROOT / "architecture" / "diagrams")
    all_rules = load_rules(ROOT / "architecture" / "rules" / "rules.yaml")
    rule = next(rule for rule in all_rules.rules if rule.id == rule_id)
    all_rules.rules = [rule]
    source = next(iter(resolve(rule.source, observed, target, all_rules)))
    target_node = next(iter(resolve(rule.target, observed, target, all_rules)))
    correct_edges = deepcopy(observed.edges)

    if mutation == "remove_required":
        observed.edges = [edge for edge in observed.edges if not (edge.source == source and edge.target == target_node)]
    elif mutation == "add_direct":
        observed.edges.append(Edge(source, target_node, "calls", "EXTRACTED", "src/regression.py"))
    else:
        bridge = "temporary_architecture_regression"
        observed.nodes[bridge] = Node(bridge, file="src/regression.py")
        observed.edges.extend([
            Edge(source, bridge, "calls", "EXTRACTED", "src/regression.py"),
            Edge(bridge, target_node, "calls", "EXTRACTED", "src/regression.py"),
        ])

    failed = evaluate(observed, target, all_rules)
    report_text = render_json(failed)
    report = json.loads(report_text)
    assert report["status"] == "FAIL"
    assert report["violations"][0]["rule_id"] == rule_id
    assert measure_tokens(report_text).count < measure_tokens((ROOT / "graphify-out" / "graph.json").read_text()).count

    observed.edges = correct_edges
    assert evaluate(observed, target, all_rules).status == "PASS"

