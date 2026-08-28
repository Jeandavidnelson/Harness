from architecture_harness.engine.context_selector import select_context
from architecture_harness.exporters.llm_context import render_llm_context
from architecture_harness.ir.architecture import TargetArchitectureIR
from architecture_harness.ir.context import ContextGraphIR
from architecture_harness.ir.graph import Edge, Node, ObservedGraphIR
from architecture_harness.ir.rules import MatchSpec, Rule, RulesIR


def test_context_is_compact_connected_and_preserves_provenance():
    observed = ObservedGraphIR(
        {name: Node(name, file=f"src/{name}.py") for name in ("PaymentController", "PaymentService", "PaymentRepository", "Unrelated")},
        [Edge("PaymentController", "PaymentService"), Edge("PaymentService", "PaymentRepository"), Edge("Unrelated", "Other")],
    )
    context = ContextGraphIR(
        {name: Node(name) for name in ("PaymentService", "Gateway", "Stripe")},
        [Edge("PaymentService", "Gateway", provenance="DECLARED_CONTEXT", source_file="contexte/runtime.mmd"), Edge("Gateway", "Stripe", provenance="DECLARED_CONTEXT", source_file="contexte/runtime.mmd")],
    )
    rules = RulesIR({"Service": MatchSpec(suffix="Service"), "Repository": MatchSpec(suffix="Repository")}, [Rule("must-repo", "required_path", "Service", "Repository")])
    compact = select_context(["PaymentService"], observed, context, TargetArchitectureIR(), rules, radius=1, max_items=10)
    rendered = render_llm_context(compact)
    assert "Unrelated" not in rendered
    assert "PaymentService -> Gateway [DECLARED; confidence=DECLARED_CONTEXT" in rendered
    assert "must-repo" in rendered
    assert len(compact.observed_edges) < len(observed.edges)
