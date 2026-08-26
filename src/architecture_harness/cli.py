from __future__ import annotations

import argparse
import sys
from pathlib import Path

from architecture_harness.adapters.graphify import GraphifyError, load_graphify
from architecture_harness.adapters.mermaid import MermaidError, load_mermaid_directory
from architecture_harness.adapters.rules import RulesError, load_rules
from architecture_harness.config import ProjectPaths


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="arch-harness")
    parser.add_argument("--root", type=Path, default=Path.cwd(), help="project root")
    sub = parser.add_subparsers(dest="command", required=True)
    sub.add_parser("observed", help="summarize Graphify output")
    sub.add_parser("target", help="print normalized target architecture")
    rules_parser = sub.add_parser("rules", help="validate or list rules")
    rules_parser.add_argument("action", choices=("validate", "list"))
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    paths = ProjectPaths(args.root.resolve())
    try:
        if args.command == "observed":
            for key, value in load_graphify(paths.observed).summary().items():
                print(f"{key}: {value}")
            return 0
        if args.command == "target":
            target = load_mermaid_directory(paths.target_dir)
            print("nodes: " + ", ".join(sorted(target.nodes)))
            print("edges:")
            for source, target_node in target.edges:
                print(f"  {source} -> {target_node}")
            print("subgraphs:")
            for name, members in sorted(target.subgraphs.items()):
                print(f"  {name}: {', '.join(sorted(members))}")
            return 0
        if args.command == "rules":
            rules = load_rules(paths.rules)
            if args.action == "validate":
                print(f"valid: {len(rules.rules)} rules, {len(rules.roles)} roles")
            else:
                for rule in rules.rules:
                    print(f"{rule.id}: {rule.type} {rule.source} -> {rule.target}")
            return 0
    except (GraphifyError, MermaidError, RulesError, ValueError, OSError) as exc:
        print(f"configuration error: {exc}", file=sys.stderr)
        return 2
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
