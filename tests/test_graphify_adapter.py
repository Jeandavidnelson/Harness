from pathlib import Path

from architecture_harness.adapters.graphify import load_graphify


def test_load_graphify_normalizes_graph():
    graph = load_graphify(Path(__file__).parent / "fixtures" / "graphify.json")
    assert set(graph.nodes) == {"OrderController", "OrderService"}
    assert graph.edges[0].relation == "calls"
    assert graph.summary() == {"nodes": 2, "edges": 1, "extracted": 1, "inferred": 0, "ambiguous": 0}

