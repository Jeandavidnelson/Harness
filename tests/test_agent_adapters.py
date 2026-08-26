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
        assert "arch-harness agent validate" in text
    assert "rules:" not in paths[1].read_text(encoding="utf-8")

