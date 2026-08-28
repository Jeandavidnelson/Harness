from architecture_harness.engine.gate import gate_payload
from architecture_harness.engine.harness import evaluate
from architecture_harness.ir.architecture import TargetArchitectureIR
from architecture_harness.ir.graph import Node, ObservedGraphIR
from architecture_harness.ir.rules import MatchSpec, Rule, RulesIR


def policy(rule: Rule) -> RulesIR:
    return RulesIR({"Future": MatchSpec(exact="future_component"), "Existing": MatchSpec(exact="existing")}, [rule])


def test_when_observed_missing_component_is_not_applicable():
    graph = ObservedGraphIR({"existing": Node("existing")}, [])
    result = evaluate(graph, TargetArchitectureIR(), policy(Rule("future", "forbidden_edge", "Existing", "Future", applicability="when_observed")))
    assert result.status == "NOT_APPLICABLE"
    assert result.exit_code == 0
    assert gate_payload(result)["rule_assessments"][0]["status"] == "NOT_APPLICABLE"


def test_required_mapping_is_unresolved_and_technical():
    graph = ObservedGraphIR({"existing": Node("existing")}, [])
    rule = Rule("must-map", "forbidden_edge", "Existing", "Future", applicability="required")
    result = evaluate(graph, TargetArchitectureIR(), policy(rule))
    assert result.status == "UNRESOLVED"
    assert result.exit_code == 2
    assessment = gate_payload(result)["rule_assessments"][0]
    assert assessment["target_matches"] == []
    assert "target mapping" in assessment["reason"]


def test_declared_only_never_evaluates_observed_code():
    graph = ObservedGraphIR({"existing": Node("existing"), "future_component": Node("future_component")}, [])
    rule = Rule("guidance", "required_edge", "Existing", "Future", applicability="declared_only")
    result = evaluate(graph, TargetArchitectureIR(), policy(rule))
    assert result.status == "NOT_APPLICABLE"
    assert not result.violations
