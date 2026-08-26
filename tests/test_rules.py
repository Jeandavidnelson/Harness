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

