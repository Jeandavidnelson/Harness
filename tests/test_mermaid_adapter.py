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


def test_official_mermaid_parser_supports_architecture_and_non_flowchart_diagrams():
    architecture = parse_mermaid("""architecture-beta
    service api(server)[API]
    service db(database)[Database]
    api:R --> L:db
    """)
    assert architecture.diagram_types == ["architecture"]
    assert architecture.edges == [("api", "db")]

    sequence = parse_mermaid("""sequenceDiagram
    participant Client
    participant API
    Client->>API: request
    """)
    assert sequence.diagram_types == ["sequence"]
    assert sequence.edges == [("Client", "API")]

    classes = parse_mermaid("classDiagram\nController --> Service\n")
    assert classes.diagram_types == ["classDiagram"]
    assert classes.edges == [("Controller", "Service")]

    entities = parse_mermaid("erDiagram\nORDER ||--o{ LINE : contains\n")
    assert entities.diagram_types == ["er"]
    assert entities.edges == [("ORDER", "LINE")]
