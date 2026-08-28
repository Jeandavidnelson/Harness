from __future__ import annotations

import re
from pathlib import Path

from architecture_harness.ir.architecture import TargetArchitectureIR
from architecture_harness.ir.graph import ObservedGraphIR


def _terms(value: str) -> set[str]:
    expanded = re.sub(r"([a-z0-9])([A-Z])", r"\1 \2", value)
    return {part.lower() for part in re.split(r"[^A-Za-z0-9]+", expanded) if len(part) > 1}


def _score(identifier: str, label: str, observed_id: str, file: str | None) -> float:
    declared = _terms(identifier) | _terms(label)
    observed = _terms(observed_id) | _terms(file or "")
    if not declared or not observed:
        return 0.0
    overlap = declared & observed
    score = len(overlap) / len(declared)
    compact_declared = re.sub(r"[^A-Za-z0-9]", "", label).lower()
    compact_identifier = re.sub(r"[^A-Za-z0-9]", "", identifier).lower()
    compact_observed = re.sub(r"[^A-Za-z0-9]", "", observed_id).lower()
    if compact_declared and compact_declared in compact_observed:
        score = max(score, 0.95)
    if compact_declared and compact_observed.endswith(compact_declared):
        score += 0.1
    if compact_identifier and compact_observed.endswith(compact_identifier):
        score += 0.3
    normalized_file = (file or "").replace("\\", "/")
    if normalized_file.startswith("src/") or "/src/" in normalized_file:
        score += 0.5
    return round(score, 3)


def build_rule_author_context(root: Path, target: TargetArchitectureIR, observed: ObservedGraphIR) -> dict[str, object]:
    mappings = []
    for identifier, label in sorted(target.nodes.items()):
        candidates = sorted((
            {
                "graphify_id": node.id,
                "file": node.file,
                "kind": node.kind,
                "score": _score(identifier, label, node.id, node.file),
            }
            for node in observed.nodes.values() if node.kind == "code"
        ), key=lambda item: (-item["score"], item["graphify_id"]))[:5]
        useful = [item for item in candidates if item["score"] > 0]
        top = useful[0]["score"] if useful else 0.0
        second = useful[1]["score"] if len(useful) > 1 else 0.0
        status = "resolved_candidate" if top >= 0.95 and top - second >= 0.05 else "ambiguous" if useful else "pending_code"
        mappings.append({
            "declared_id": identifier,
            "declared_label": label,
            "status": status,
            "candidates": useful,
        })
    diagrams = []
    for source in target.sources:
        path = Path(source)
        diagrams.append({
            "path": str(path),
            "text": path.read_text(encoding="utf-8") if path.is_file() else "",
        })
    return {
        "status": "PASS",
        "diagram_types": target.diagram_types,
        "declared_facts": {
            "nodes": [{"id": key, "label": value} for key, value in sorted(target.nodes.items())],
            "edges": [{"source": source, "target": destination} for source, destination in target.edges],
            "subgraphs": {key: sorted(value) for key, value in sorted(target.subgraphs.items())},
        },
        "mapping_proposals": mappings,
        "diagrams": diagrams,
        "instructions": {
            "resolved_candidate": "Verify evidence, then write an exact candidate matcher.",
            "ambiguous": "Use diagram semantics and candidate files; ask the human only if ambiguity remains.",
            "pending_code": "Keep applicability when_observed and retry after code plus Graphify refresh.",
        },
    }
