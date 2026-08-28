import tomllib
from pathlib import Path

import pytest

from architecture_harness.integrations import IntegrationError, install_bmad, install_claude, install_codex


ROOT = Path(__file__).parents[1]


def test_bmad_overrides_match_real_customization_surface():
    for path in sorted((ROOT / "integrations" / "bmad" / "overrides").glob("*.toml")):
        workflow = tomllib.loads(path.read_text(encoding="utf-8"))["workflow"]
        assert set(workflow) <= {"activation_steps_append", "persistent_facts", "on_complete"}
        assert "arch-harness" in path.read_text(encoding="utf-8")


def test_bmad_installer_is_pluggable_and_non_destructive(tmp_path):
    (tmp_path / "_bmad" / "custom").mkdir(parents=True)
    payload = install_bmad(tmp_path, ROOT)
    assert payload["core_dependency_added"] is False
    assert len(payload["installed"]) == 5
    assert (tmp_path / ".agents" / "skills" / "architecture-rule-author" / "SKILL.md").is_file()
    with pytest.raises(IntegrationError, match="Refusing to overwrite"):
        install_bmad(tmp_path, ROOT)


def test_bmad_installer_requires_real_bmad_layout(tmp_path):
    with pytest.raises(IntegrationError, match="BMAD is not installed"):
        install_bmad(tmp_path, ROOT)


def test_codex_and_claude_install_the_rule_author_and_project_instructions(tmp_path):
    codex = tmp_path / "codex"
    claude = tmp_path / "claude"
    codex.mkdir()
    claude.mkdir()
    install_codex(codex, ROOT)
    install_claude(claude, ROOT)
    assert (codex / ".agents/skills/architecture-rule-author/SKILL.md").is_file()
    assert "$architecture-rule-author" in (codex / "AGENTS.md").read_text()
    assert (claude / ".claude/skills/architecture-rule-author/SKILL.md").is_file()
    assert (claude / ".claude/skills/architecture-harness/SKILL.md").is_file()
    assert "architecture-rule-author" in (claude / "CLAUDE.md").read_text()
