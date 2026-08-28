from __future__ import annotations

import shutil
import subprocess
import time
from pathlib import Path

from architecture_harness.adapters.graphify import load_graphify
from architecture_harness.graph_freshness import check_graph_freshness


class GraphifyRuntimeError(ValueError):
    pass


def resolve_graphify(root: Path) -> Path:
    project_binary = root / ".venv" / "bin" / "graphify"
    if project_binary.is_file():
        return project_binary
    system_binary = shutil.which("graphify")
    if system_binary:
        return Path(system_binary)
    raise GraphifyRuntimeError("Graphify executable not found; install project development dependencies")


def refresh_command(root: Path, graphify: Path) -> list[str]:
    if (root / "graphify-out" / "manifest.json").is_file():
        return [str(graphify), "update", str(root), "--no-cluster"]
    return [str(graphify), "extract", str(root), "--code-only", "--no-cluster"]


def refresh_graph(root: Path) -> dict[str, object]:
    root = root.resolve()
    graphify = resolve_graphify(root)
    command = refresh_command(root, graphify)
    started = time.perf_counter()
    process = subprocess.run(command, text=True, capture_output=True)
    duration = round(time.perf_counter() - started, 4)
    if process.returncode != 0:
        raise GraphifyRuntimeError(
            f"Graphify refresh failed with exit {process.returncode}: {process.stderr.strip()}"
        )
    freshness = check_graph_freshness(root)
    if not freshness.fresh:
        changed = freshness.stale_files + freshness.missing_files
        raise GraphifyRuntimeError("Graphify refresh completed but graph remains stale: " + ", ".join(changed))
    summary = load_graphify(root / "graphify-out" / "graph.json").summary()
    return {
        "status": "PASS",
        "mode": "update" if "update" in command else "extract",
        "command": command,
        "graph": str(root / "graphify-out" / "graph.json"),
        "fresh": True,
        "summary": summary,
        "duration_seconds": duration,
        "stdout": process.stdout.strip(),
    }

