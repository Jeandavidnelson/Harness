from architecture_harness.adapters.rules import load_rules
from architecture_harness.engine.matcher import resolve
from architecture_harness.ir.architecture import TargetArchitectureIR
from architecture_harness.ir.graph import Node, ObservedGraphIR


def test_rules_and_explicit_role_mapping(tmp_path):
    path = tmp_path / "rules.yaml"
    path.write_text("""roles:
  Controller:
    match:
      suffix: Controller
rules:
  - id: no-direct
    type: forbidden_edge
    source: Controller
    target: Repo
    allowed_targets: [AuditRepo]
""")
    rules = load_rules(path)
    graph = ObservedGraphIR(nodes={"OrderController": Node("OrderController"), "OrderService": Node("OrderService")})
    assert resolve("Controller", graph, TargetArchitectureIR(), rules) == {"OrderController"}
    assert rules.rules[0].allowed_targets == ("AuditRepo",)


def test_v2_rule_lifecycle_fields_and_defaults(tmp_path):
    path = tmp_path / "rules.yaml"
    path.write_text("""roles:
rules:
  - id: candidate-boundary
    type: forbidden_path
    source: A
    target: B
    severity: warning
    scope: [src]
    exceptions: [migration]
    rationale: Keep the boundary explicit
    provenance: GENERATED
    status: candidate
    applicability: when_observed
""")
    rule = load_rules(path).rules[0]
    assert rule.severity == "warning"
    assert rule.scope == ("src",)
    assert rule.exceptions == ("migration",)
    assert rule.rationale == "Keep the boundary explicit"
    assert rule.provenance == "GENERATED"
    assert rule.status == "candidate"
    assert rule.applicability == "when_observed"
    assert rule.blocking is False
