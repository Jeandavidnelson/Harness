import json
from pathlib import Path

from architecture_harness.adapters.graphify import load_graphify
from architecture_harness.engine.harness import evaluate
from architecture_harness.exporters.json import render_json
from architecture_harness.ir.architecture import TargetArchitectureIR
from architecture_harness.ir.graph import Edge
from architecture_harness.ir.rules import MatchSpec, Rule, RulesIR


def test_compact_report_enables_one_iteration_fix():
    observed = load_graphify(Path(__file__).parent / "fixtures" / "graph_violation.json")
    rules = RulesIR(
        {"Controller": MatchSpec(suffix="Controller"), "Repository": MatchSpec(suffix="Repository")},
        [Rule("controller-no-repository", "forbidden_edge", "Controller", "Repository")],
    )
    failure = evaluate(observed, TargetArchitectureIR(), rules)
    report = json.loads(render_json(failure))
    assert report["status"] == "FAIL"
    assert report["violations"][0]["observed_path"] == ["OrderController", "OrderRepository"]
    assert report["violations"][0]["files"] == ["src/order/controller.py", "src/order/repository.py"]
    observed.edges = [Edge("OrderController", "OrderService")]
    assert evaluate(observed, TargetArchitectureIR(), rules).status == "PASS"

