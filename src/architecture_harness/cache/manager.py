from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any, Callable


class CacheManager:
    def __init__(self, directory: Path):
        self.directory = directory

    @staticmethod
    def digest(paths: list[Path]) -> str:
        digest = hashlib.sha256()
        for path in sorted(paths):
            digest.update(str(path).encode())
            digest.update(path.read_bytes())
        return digest.hexdigest()

    def get(self, namespace: str, paths: list[Path]) -> Any | None:
        key = self.digest(paths)
        cache_path = self.directory / f"{namespace}-{key}.json"
        try:
            return json.loads(cache_path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError):
            return None

    def put(self, namespace: str, paths: list[Path], value: Any) -> None:
        self.directory.mkdir(parents=True, exist_ok=True)
        key = self.digest(paths)
        (self.directory / f"{namespace}-{key}.json").write_text(json.dumps(value, indent=2), encoding="utf-8")

