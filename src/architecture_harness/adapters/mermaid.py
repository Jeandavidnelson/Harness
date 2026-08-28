from __future__ import annotations

import json
import shutil
import subprocess
from pathlib import Path

from architecture_harness.ir.architecture import TargetArchitectureIR


class MermaidError(ValueError):
    pass


def parse_mermaid(text: str, source: str = "<memory>") -> TargetArchitectureIR:
    node = shutil.which("node")
    if not node:
        raise MermaidError("Node.js is required by the official Mermaid parser runtime")
    bridge = Path(__file__).parents[1] / "runtime" / "mermaid_bridge.mjs"
    try:
        completed = subprocess.run(
            [node, str(bridge)], input=json.dumps({"text": text, "source": source}),
            text=True, capture_output=True, check=False,
        )
    except OSError as exc:
        raise MermaidError(f"Cannot execute official Mermaid parser: {exc}") from exc
    if completed.returncode:
        detail = completed.stderr.strip().splitlines()[-1] if completed.stderr.strip() else "unknown parse error"
        raise MermaidError(f"{source}: Mermaid parser rejected diagram: {detail}")
    try:
        payload = json.loads(completed.stdout)
    except json.JSONDecodeError as exc:
        raise MermaidError(f"{source}: invalid response from official Mermaid parser") from exc
    return TargetArchitectureIR(
        nodes={item["id"]: item["label"] for item in payload["nodes"]},
        edges=[(item["source"], item["target"]) for item in payload["edges"]],
        subgraphs={name: set(members) for name, members in payload["subgraphs"].items()},
        sources=[source],
        diagram_types=[payload["diagram_type"]],
    )


def load_mermaid_directory(directory: str | Path) -> TargetArchitectureIR:
    result = TargetArchitectureIR()
    files = sorted(Path(directory).glob("*.mmd"))
    if not files:
        raise MermaidError(f"No Mermaid files found in {directory}")
    for path in files:
        parsed = parse_mermaid(path.read_text(encoding="utf-8"), str(path))
        result.nodes.update(parsed.nodes)
        result.edges.extend(edge for edge in parsed.edges if edge not in result.edges)
        for name, members in parsed.subgraphs.items():
            result.subgraphs.setdefault(name, set()).update(members)
        result.sources.extend(parsed.sources)
        result.diagram_types.extend(parsed.diagram_types)
    return result
