from pathlib import Path

from architecture_harness.cli import main


ROOT = Path(__file__).parents[1]
SKILL = ROOT / "skills" / "architecture-rule-author" / "SKILL.md"


def test_rule_author_skill_preserves_human_validation_boundary(capsys):
    text = SKILL.read_text(encoding="utf-8")
    assert "Never promote" in text
    assert "status: candidate" in text
    assert "provenance: GENERATED" in text
    assert "explicit human approval" in text
    assert main([
        "--root", str(ROOT), "rules", "validate",
        "--file", str(ROOT / "architecture" / "rules" / "candidates.yaml"),
    ]) == 0
    assert "valid: 1 rules" in capsys.readouterr().out
