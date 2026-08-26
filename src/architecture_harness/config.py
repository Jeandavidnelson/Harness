from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class ProjectPaths:
    root: Path

    @property
    def observed(self) -> Path:
        return self.root / "graphify-out" / "graph.json"

    @property
    def target_dir(self) -> Path:
        return self.root / "architecture" / "diagrams"

    @property
    def rules(self) -> Path:
        return self.root / "architecture" / "rules" / "rules.yaml"

    @property
    def context_dir(self) -> Path:
        return self.root / "contexte"

