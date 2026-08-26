from architecture_harness.engine.harness import evaluate
from architecture_harness.ir.architecture import TargetArchitectureIR
from architecture_harness.ir.graph import Edge, Node, ObservedGraphIR
from architecture_harness.ir.rules import MatchSpec, Rule, RulesIR


ROLES = {
    "Controller": MatchSpec(suffix="Controller"), "Service": MatchSpec(suffix="Service"),
    "Repository": MatchSpec(suffix="Repository"), "Domain": MatchSpec(suffix="Domain"),
    "Infrastructure": MatchSpec(suffix="Infrastructure"),
}


def graph(edges):
    ids = {node for edge in edges for node in edge}
    return ObservedGraphIR({node: Node(node, file=f"src/{node}.py") for node in ids}, [Edge(*edge) for edge in edges])


def run(edges, rule):
    return evaluate(graph(edges), TargetArchitectureIR(), RulesIR(ROLES, [rule]))


def test_pass_architecture_and_extra_allowed_dependency():
    edges = [("OrderController", "OrderService"), ("OrderService", "OrderRepository"), ("OrderService", "Logger")]
    rules = RulesIR(ROLES, [
        Rule("no-direct", "forbidden_edge", "Controller", "Repository"),
        Rule("must-repo", "required_path", "Service", "Repository"),
        Rule("must-service", "required_edge", "Controller", "Service"),
    ])
    assert evaluate(graph(edges), TargetArchitectureIR(), rules).status == "PASS"


def test_direct_violation_with_evidence():
    result = run([("OrderController", "OrderRepository")], Rule("no-direct", "forbidden_edge", "Controller", "Repository"))
    assert result.status == "FAIL"
    assert result.violations[0].observed_path == ("OrderController", "OrderRepository")


def test_indirect_forbidden_path():
    result = run([("SalesDomain", "Bridge"), ("Bridge", "SqlInfrastructure")], Rule("isolate", "forbidden_path", "Domain", "Infrastructure"))
    assert result.violations[0].observed_path == ("SalesDomain", "Bridge", "SqlInfrastructure")


def test_missing_required_dependency():
    result = run([("OrderService", "Logger")], Rule("must-repo", "required_path", "Service", "Repository"))
    assert result.status == "FAIL"
    assert result.violations[0].target == "Repository"


def test_ambiguous_edges_do_not_hard_fail():
    observed = ObservedGraphIR({"OrderController": Node("OrderController"), "OrderRepository": Node("OrderRepository")}, [Edge("OrderController", "OrderRepository", provenance="AMBIGUOUS")])
    result = evaluate(observed, TargetArchitectureIR(), RulesIR(ROLES, [Rule("no-direct", "forbidden_edge", "Controller", "Repository")]))
    assert result.status == "PASS"


def test_pass_fail_pass_lifecycle():
    policy = RulesIR(ROLES, [Rule("no-direct", "forbidden_edge", "Controller", "Repository")])
    correct = graph([("OrderController", "OrderService"), ("OrderService", "OrderRepository")])
    assert evaluate(correct, TargetArchitectureIR(), policy).status == "PASS"
    changed = graph([("OrderController", "OrderService"), ("OrderService", "OrderRepository"), ("OrderController", "OrderRepository")])
    assert evaluate(changed, TargetArchitectureIR(), policy).status == "FAIL"
    assert evaluate(correct, TargetArchitectureIR(), policy).status == "PASS"
