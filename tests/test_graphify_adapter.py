from pathlib import Path

from architecture_harness.adapters.graphify import load_graphify


def test_load_graphify_normalizes_graph():
    graph = load_graphify(Path(__file__).parent / "fixtures" / "graphify.json")
    assert set(graph.nodes) == {"OrderController", "OrderService"}
    assert graph.edges[0].relation == "calls"
    assert graph.summary() == {"nodes": 2, "edges": 1, "extracted": 1, "inferred": 0, "ambiguous": 0}


def test_load_real_graphify_schema(tmp_path):
    path = tmp_path / "graph.json"
    path.write_text('''{"nodes":[{"id":"module","type":"code","source_file":"src/module.py"}],"edges":[{"source":"module","target":"symbol","relation":"contains","confidence":"INFERRED","source_file":"src/module.py"}]}''')
    graph = load_graphify(path)
    assert graph.nodes["module"].file == "src/module.py"
    assert graph.nodes["module"].kind == "code"
    assert graph.edges[0].provenance == "INFERRED"
    assert graph.edges[0].evidence_origin.value == "INFERRED"


def test_load_networkx_links_schema(tmp_path):
    path = tmp_path / "graph.json"
    path.write_text('{"nodes":[{"id":"A"}],"links":[{"source":"A","target":"B","confidence":"EXTRACTED"}]}')
    graph = load_graphify(path)
    assert len(graph.edges) == 1
    assert set(graph.nodes) == {"A", "B"}
    assert graph.edges[0].evidence_origin.value == "OBSERVED"
