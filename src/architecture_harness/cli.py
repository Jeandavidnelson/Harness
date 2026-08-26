from __future__ import annotations

import argparse
import sys
from pathlib import Path

from architecture_harness.adapters.graphify import GraphifyError, load_graphify
from architecture_harness.adapters.mermaid import MermaidError, load_mermaid_directory
from architecture_harness.config import ProjectPaths


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="arch-harness")
    parser.add_argument("--root", type=Path, default=Path.cwd(), help="project root")
    sub = parser.add_subparsers(dest="command", required=True)
    sub.add_parser("observed", help="summarize Graphify output")
    sub.add_parser("target", help="print normalized target architecture")
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
    except (GraphifyError, MermaidError, ValueError, OSError) as exc:
        print(f"configuration error: {exc}", file=sys.stderr)
        return 2
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
