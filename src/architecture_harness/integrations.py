from __future__ import annotations

import shutil
from pathlib import Path


class IntegrationError(ValueError):
    pass


def install_bmad(project_root: Path, adapter_root: Path, force: bool = False) -> dict[str, object]:
    bmad_root = project_root / "_bmad"
    if not bmad_root.is_dir():
        raise IntegrationError("BMAD is not installed: run `npx bmad-method install` first")
    source = adapter_root / "integrations" / "bmad" / "overrides"
    destination = bmad_root / "custom"
    destination.mkdir(parents=True, exist_ok=True)
    installed: list[str] = []
    for template in sorted(source.glob("*.toml")):
        target = destination / template.name
        if target.exists() and not force:
            raise IntegrationError(f"Refusing to overwrite existing BMAD override {target}; use --force after review")
        shutil.copy2(template, target)
        installed.append(str(target.relative_to(project_root)))
    installed.extend(_install_rule_author_skill(project_root, adapter_root, ".agents/skills", force))
    return {"status": "PASS", "integration": "bmad", "installed": installed, "core_dependency_added": False}


def _copy_tree(source: Path, target: Path, project_root: Path, force: bool) -> list[str]:
    if target.exists():
        if not force:
            raise IntegrationError(f"Refusing to overwrite existing orchestrator asset {target}; use --force after review")
        shutil.rmtree(target)
    shutil.copytree(source, target)
    return [str(path.relative_to(project_root)) for path in sorted(target.rglob("*")) if path.is_file()]


def _install_rule_author_skill(project_root: Path, adapter_root: Path, destination: str, force: bool) -> list[str]:
    source = adapter_root / "skills" / "architecture-rule-author"
    if not source.is_dir():
        raise IntegrationError(f"Architecture Rule Author skill not found at {source}")
    return _copy_tree(source, project_root / destination / "architecture-rule-author", project_root, force)


def _install_project_instructions(project_root: Path, source: Path, target_name: str) -> list[str]:
    target = project_root / target_name
    marker = "<!-- architecture-harness-managed -->"
    content = source.read_text(encoding="utf-8").strip()
    if target.is_file() and marker in target.read_text(encoding="utf-8"):
        return []
    prefix = target.read_text(encoding="utf-8").rstrip() + "\n\n" if target.is_file() else ""
    target.write_text(f"{prefix}{marker}\n{content}\n", encoding="utf-8")
    return [str(target.relative_to(project_root))]


def install_codex(project_root: Path, adapter_root: Path, force: bool = False) -> dict[str, object]:
    installed = _install_rule_author_skill(project_root, adapter_root, ".agents/skills", force)
    installed += _install_project_instructions(
        project_root, adapter_root / "integrations" / "codex" / "AGENTS.snippet.md", "AGENTS.md",
    )
    return {"status": "PASS", "integration": "codex", "installed": installed, "core_dependency_added": False}


def install_claude(project_root: Path, adapter_root: Path, force: bool = False) -> dict[str, object]:
    installed = _install_rule_author_skill(project_root, adapter_root, ".claude/skills", force)
    installed += _copy_tree(
        adapter_root / "integrations" / "claude" / "architecture-harness",
        project_root / ".claude" / "skills" / "architecture-harness",
        project_root, force,
    )
    installed += _install_project_instructions(
        project_root, adapter_root / "integrations" / "claude" / "SKILL.md", "CLAUDE.md",
    )
    return {"status": "PASS", "integration": "claude", "installed": installed, "core_dependency_added": False}
