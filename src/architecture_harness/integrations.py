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
    return {"status": "PASS", "integration": "bmad", "installed": installed, "core_dependency_added": False}
