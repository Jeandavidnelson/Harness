from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass
from pathlib import Path



@dataclass(frozen=True)
class FreshnessResult:
    stale_files: tuple[str, ...]
    missing_files: tuple[str, ...]

    @property
    def fresh(self) -> bool:
        return not self.stale_files and not self.missing_files


def check_graph_freshness(root: Path, manifest_path: Path | None = None) -> FreshnessResult:
    manifest_path = manifest_path or root / "graphify-out" / "manifest.json"
    try:
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise ValueError(f"Graphify manifest unavailable or invalid: {exc}") from exc

    stale: list[str] = []
    missing: list[str] = []
    code_manifest = {
        relative: metadata for relative, metadata in manifest.items()
        if relative == "pyproject.toml" or Path(relative).suffix in {".py", ".sh"}
    }
    for relative, metadata in code_manifest.items():
        path = root / relative
        if not path.exists():
            stale.append(relative)
            continue
        current = hashlib.md5(path.read_bytes()).hexdigest()
        if current != metadata.get("ast_hash"):
            stale.append(relative)

    candidates = [root / "pyproject.toml"]
    for directory in (root / "src", root / "tests", root / "scripts"):
        if directory.exists():
            candidates.extend(path for path in directory.rglob("*") if path.suffix in {".py", ".sh"})
    for path in candidates:
        if path.is_file():
            relative = path.relative_to(root).as_posix()
            if relative not in manifest:
                missing.append(relative)
    return FreshnessResult(tuple(sorted(stale)), tuple(sorted(missing)))
