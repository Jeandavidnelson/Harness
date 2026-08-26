from __future__ import annotations

import re
from pathlib import Path

from architecture_harness.ir.architecture import TargetArchitectureIR


class MermaidError(ValueError):
    pass


HEADER = re.compile(r"^(?:flowchart|graph)\s+(LR|RL|TB|TD|BT)\s*$", re.I)
NODE = re.compile(r'^([A-Za-z_][\w.-]*)(?:\s*(?:\[([^]]*)\]|\(([^)]*)\)|\{([^}]*)\}))?$')
EDGE = re.compile(r"\s*(?:--(?:[^>-]*?)--?>|-->|==>|-.->)\s*")


def _node(token: str) -> tuple[str, str]:
    token = token.strip()
    match = NODE.match(token)
    if not match:
        raise MermaidError(f"Unsupported Mermaid node syntax: {token}")
    identifier = match.group(1)
    return identifier, next((value for value in match.groups()[1:] if value is not None), identifier)


def parse_mermaid(text: str, source: str = "<memory>") -> TargetArchitectureIR:
    graph = TargetArchitectureIR(sources=[source])
    current: str | None = None
    header_seen = False
    for number, raw_line in enumerate(text.splitlines(), 1):
        line = raw_line.split("%%", 1)[0].strip().rstrip(";")
        if not line:
            continue
        if not header_seen:
            if not HEADER.match(line):
                raise MermaidError(f"{source}:{number}: expected flowchart/graph header")
            header_seen = True
            continue
        if line.lower().startswith("subgraph "):
            name, _ = _node(line[9:].strip())
            current = name
            graph.subgraphs.setdefault(name, set())
            continue
        if line.lower() == "end":
            current = None
            continue
        if line.startswith(("direction ", "classDef ", "class ", "style ", "linkStyle ")):
            continue
        parts = EDGE.split(line)
        if len(parts) > 1:
            parsed = [_node(part) for part in parts]
            for identifier, label in parsed:
                graph.nodes[identifier] = label
                if current:
                    graph.subgraphs[current].add(identifier)
            graph.edges.extend((parsed[i][0], parsed[i + 1][0]) for i in range(len(parsed) - 1))
        else:
            identifier, label = _node(line)
            graph.nodes[identifier] = label
            if current:
                graph.subgraphs[current].add(identifier)
    if not header_seen:
        raise MermaidError(f"{source}: empty Mermaid graph")
    return graph


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
    return result

