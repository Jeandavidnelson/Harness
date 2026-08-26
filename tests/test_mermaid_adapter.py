from architecture_harness.adapters.mermaid import parse_mermaid


def test_parse_nodes_edges_labels_and_subgraphs():
    result = parse_mermaid("""flowchart LR
    subgraph App[Application]
      Controller[HTTP Controller] --> Service
    end
    Service --> Repository
    """)
    assert result.nodes["Controller"] == "HTTP Controller"
    assert result.edges == [("Controller", "Service"), ("Service", "Repository")]
    assert result.subgraphs["App"] == {"Controller", "Service"}

