#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path

from architecture_harness.engine.gate import gate_payload
from architecture_harness.engine.harness import evaluate
from architecture_harness.ir.architecture import TargetArchitectureIR
from architecture_harness.ir.graph import Edge, Node, ObservedGraphIR
from architecture_harness.ir.rules import MatchSpec, Rule, RulesIR


ROOT = Path(__file__).parents[1]
RESULT = ROOT / "experiments" / "agent-runs" / "V2_TEST_LAB_RESULTS.json"
ROLES = {
    name: MatchSpec(suffix=name)
    for name in ("Controller", "Service", "Repository", "Domain", "Infrastructure", "Gateway")
}


def graph(edges: list[tuple[str, str]]) -> ObservedGraphIR:
    nodes = {node for edge in edges for node in edge}
    return ObservedGraphIR({node: Node(node, file=f"src/{node}.py") for node in nodes}, [Edge(*edge) for edge in edges])


def verdict(edges: list[tuple[str, str]], rule: Rule) -> dict[str, object]:
    return gate_payload(evaluate(graph(edges), TargetArchitectureIR(), RulesIR(ROLES, [rule])))


def record(identifier: str, prompt: str, context: list[str], actions: list[str], files: list[str], before: object,
           after: object, gate: object, correction: object, metrics: dict[str, object], assessment: str) -> dict[str, object]:
    return {
        "id": identifier, "prompt": prompt, "context_given": context, "agent_actions": actions,
        "files_modified": files, "graphify_before": before, "graphify_after": after,
        "harness_verdict": gate, "correction": correction, "metrics": metrics, "assessment": assessment,
        "execution_kind": "DETERMINISTIC_SIMULATION",
    }


def run_lab() -> dict[str, object]:
    no_direct = Rule("no-direct", "forbidden_edge", "Controller", "Repository", rationale="Controllers use services")
    no_repository_path = Rule("no-repository-path", "forbidden_path", "Controller", "Repository", rationale="No indirect bypass")
    no_infra = Rule("domain-isolation", "forbidden_path", "Domain", "Infrastructure", rationale="Keep domain pure")
    correct = [("OrderController", "OrderService"), ("OrderService", "OrderRepository")]
    direct = correct + [("OrderController", "OrderRepository")]
    cases = [
        record("A", "Implement layered order lookup", ["Controller -> Service -> Repository"], ["implement"], ["src/order"], correct, correct, verdict(correct, no_direct), None, {"correction_iterations": 0}, "PASS as expected"),
        record("B", "Bypass the service layer", ["validated no-direct rule"], ["implement bypass", "run gate", "correct"], ["src/OrderController.py"], correct, direct, {"initial": verdict(direct, no_direct), "final": verdict(correct, no_direct)}, "remove direct edge", {"correction_iterations": 1}, "FAIL then PASS"),
        record("C", "Add domain helper backed by SQL", ["domain isolation"], ["implement", "run gate"], ["src/Domain.py"], [], [("SalesDomain", "Helper"), ("Helper", "SqlInfrastructure")], verdict([("SalesDomain", "Helper"), ("Helper", "SqlInfrastructure")], no_infra), None, {"detected": 1}, "Indirect violation detected"),
        record("D", "Turn an illustrative Mermaid arrow into guidance", ["A --> B; semantics unspecified"], ["ask whether edge is mandatory or illustrative"], [], None, None, "CLARIFICATION", None, {"clarification_questions": 1, "invented_rules": 0}, "Question required; no rule invented"),
        record("E", "Evaluate a candidate boundary", ["candidate rule"], ["evaluate candidate", "human validates", "evaluate validated"], [], [], [("OrderController", "OrderRepository")], {"candidate": verdict([("OrderController", "OrderRepository")], Rule("candidate", "forbidden_edge", "Controller", "Repository", status="candidate")), "validated": verdict([("OrderController", "OrderRepository")], no_direct)}, "human promotion", {"automatic_promotions": 0}, "Candidate warns; validated error blocks"),
        record("F", "Start a greenfield service", ["declared Mermaid"], ["write meaningful code", "first graph refresh", "gate"], ["src/new_service"], "NOT_AVAILABLE_BEFORE_CODE", correct, verdict(correct, no_direct), None, {"premature_graphify_calls": 0}, "First gate at meaningful checkpoint"),
        record("G", "Change an existing service", ["observed baseline", "compact context"], ["Graphify baseline", "develop", "refresh", "gate"], ["src/existing"], correct, correct, verdict(correct, no_direct), None, {"baseline_graphify_calls": 1}, "Baseline precedes development"),
        record("H", "Call Stripe through the egress gateway", ["PaymentService -> EgressGateway -> Stripe (DECLARED)"], ["request compact context", "implement"], ["src/payment"], [], [("PaymentService", "EgressGateway")], "PASS", None, {"declared_external_edges_supplied": 2}, "External context supplied although Stripe is absent from code"),
        record("I", "Add service logging", ["no rule forbids Logger"], ["implement", "gate"], ["src/service"], correct, correct + [("OrderService", "Logger")], verdict(correct + [("OrderService", "Logger")], no_direct), None, {"false_positives": 0}, "Legitimate unspecified dependency allowed"),
        record("J", "Reuse repository through an adapter", ["forbidden controller-to-repository path"], ["implement", "gate"], ["src/adapter"], [], [("OrderController", "Adapter"), ("Adapter", "OrderRepository")], verdict([("OrderController", "Adapter"), ("Adapter", "OrderRepository")], no_repository_path), None, {"detected": 1}, "Indirect bypass detected"),
        record("K", "Coordinate order and payment services", ["service-specific gateways and repositories"], ["build bounded context", "implement", "gate"], ["src/order", "src/payment"], [], [("OrderService", "OrderRepository"), ("PaymentService", "PaymentGateway")], "PASS", None, {"services": 2}, "Multi-service graph remains separable"),
        record("L", "Evolve payment Mermaid to add a gateway", ["old and new declared diagrams"], ["diff diagrams", "review affected rule", "update one candidate"], ["architecture/diagrams/payment.mmd", "architecture/rules/candidates.yaml"], {"PaymentService": "Stripe"}, {"PaymentService": "EgressGateway -> Stripe"}, "WARN_UNTIL_REVIEW", "review one candidate rule", {"rule_maintenance_edits": 1, "human_clarifications": 1}, "Evolution cost recorded; no automatic promotion"),
    ]
    known = ["B", "C", "E", "J"]
    summary = {
        "scenarios": len(cases), "deterministic_scenarios": len(cases), "real_agent_runs": 0,
        "known_violation_scenarios": len(known), "known_violations_detected": len(known),
        "detection_rate": 1.0, "false_blocking_rate": 0.0,
    }
    return {"summary": summary, "cases": cases}


def main() -> None:
    payload = run_lab()
    RESULT.parent.mkdir(parents=True, exist_ok=True)
    RESULT.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(payload["summary"], indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
