from pathlib import Path

from architecture_harness.adapters.graphify import load_graphify
from architecture_harness.adapters.mermaid import parse_mermaid
from architecture_harness.engine.rule_author_context import build_rule_author_context


ROOT = Path(__file__).parents[1]


def test_author_context_ranks_real_graphify_mappings_and_preserves_source(tmp_path):
    diagram = tmp_path / "target.mmd"
    diagram.write_text("flowchart LR\nCliMain --> RulesLoad\n", encoding="utf-8")
    target = parse_mermaid(diagram.read_text(), str(diagram))
    payload = build_rule_author_context(ROOT, target, load_graphify(ROOT / "graphify-out" / "graph.json"))
    assert payload["diagrams"][0]["text"].startswith("flowchart")
    cli = next(item for item in payload["mapping_proposals"] if item["declared_id"] == "CliMain")
    assert cli["candidates"][0]["graphify_id"] == "src_architecture_harness_cli_main"
    assert cli["status"] == "resolved_candidate"
