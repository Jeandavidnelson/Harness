from pathlib import Path


ROOT = Path(__file__).parents[1]


def test_agent_adapters_use_universal_contract_without_policy_logic():
    paths = [
        ROOT / "AGENTS.md",
        ROOT / "integrations" / "claude" / "architecture-harness" / "SKILL.md",
        ROOT / "integrations" / "bmad" / "workflow-snippet.md",
    ]
    for path in paths:
        text = path.read_text(encoding="utf-8")
        assert "arch-harness agent context" in text
        assert "arch-harness agent validate" in text or "arch-harness gate" in text
    assert "rules:" not in paths[1].read_text(encoding="utf-8")


def test_v2_portability_adapters_share_exact_cli_contract():
    paths = [
        ROOT / "integrations" / "codex" / "AGENTS.snippet.md",
        ROOT / "integrations" / "claude" / "SKILL.md",
        ROOT / "integrations" / "generic" / "README.md",
        ROOT / "integrations" / "bmad" / "architecture-harness-gate.md",
    ]
    for path in paths:
        text = path.read_text(encoding="utf-8")
        assert "arch-harness graph refresh --format json" in text
        assert "arch-harness gate --format json" in text
    for path in paths[:3]:
        assert "arch-harness agent context --focus <relevant-node> --format json" in path.read_text(encoding="utf-8")


def test_core_source_has_no_orchestrator_imports():
    source = "\n".join(path.read_text(encoding="utf-8") for path in (ROOT / "src").rglob("*.py"))
    assert "import bmad" not in source.lower()
    assert "import claude" not in source.lower()
