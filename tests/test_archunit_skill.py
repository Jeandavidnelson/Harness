from pathlib import Path


ROOT = Path(__file__).parents[1]


def test_archunit_is_an_external_human_reviewed_skill():
    skill = (ROOT / "integrations" / "archunit" / "SKILL.md").read_text(encoding="utf-8")
    assert "status: validated" in skill
    assert "provenance: USER_CONFIRMED" in skill
    assert "Generated tests are candidates for human review" in skill
    assert "no Java or ArchUnit runtime dependency" in skill


def test_core_does_not_reference_archunit():
    source = "\n".join(path.read_text(encoding="utf-8") for path in (ROOT / "src").rglob("*.py"))
    assert "archunit" not in source.lower()
