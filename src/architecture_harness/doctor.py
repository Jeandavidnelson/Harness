from __future__ import annotations

from pathlib import Path

from architecture_harness.adapters.context_mermaid import load_context_directory
from architecture_harness.adapters.graphify import load_graphify
from architecture_harness.adapters.mermaid import load_mermaid_directory
from architecture_harness.adapters.rules import load_rules
from architecture_harness.config import ProjectPaths
from architecture_harness.graph_freshness import check_graph_freshness


def diagnose(paths: ProjectPaths) -> list[tuple[str, bool, str]]:
    checks: list[tuple[str, bool, str]] = []
    loaders = [
        ("Graphify output", lambda: load_graphify(paths.observed)),
        ("target Mermaid", lambda: load_mermaid_directory(paths.target_dir)),
        ("context Mermaid", lambda: load_context_directory(paths.context_dir)),
        ("rules and mappings", lambda: load_rules(paths.rules)),
    ]
    for name, loader in loaders:
        try:
            value = loader()
            detail = "valid"
            if name == "rules and mappings":
                references = {r.source for r in value.rules} | {r.target for r in value.rules}
                target = load_mermaid_directory(paths.target_dir)
                invalid = references - value.roles.keys() - target.nodes.keys() - target.subgraphs.keys()
                if invalid:
                    raise ValueError("unmapped references: " + ", ".join(sorted(invalid)))
            checks.append((name, True, detail))
        except Exception as exc:
            checks.append((name, False, str(exc)))
    try:
        freshness = check_graph_freshness(paths.root)
        if not freshness.fresh:
            changed = freshness.stale_files + freshness.missing_files
            raise ValueError("stale graph inputs: " + ", ".join(changed))
        checks.append(("Graphify freshness", True, "manifest hashes match source files"))
    except Exception as exc:
        checks.append(("Graphify freshness", False, str(exc)))
    try:
        cache = paths.root / ".cache" / "architecture-harness"
        cache.mkdir(parents=True, exist_ok=True)
        probe = cache / ".doctor"
        probe.write_text("ok", encoding="utf-8")
        probe.unlink()
        checks.append(("cache", True, "writable"))
    except OSError as exc:
        checks.append(("cache", False, str(exc)))
    return checks
