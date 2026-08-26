from __future__ import annotations

import argparse
import sys
from pathlib import Path

from architecture_harness.adapters.graphify import GraphifyError, load_graphify
from architecture_harness.config import ProjectPaths


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="arch-harness")
    parser.add_argument("--root", type=Path, default=Path.cwd(), help="project root")
    sub = parser.add_subparsers(dest="command", required=True)
    sub.add_parser("observed", help="summarize Graphify output")
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    paths = ProjectPaths(args.root.resolve())
    try:
        if args.command == "observed":
            for key, value in load_graphify(paths.observed).summary().items():
                print(f"{key}: {value}")
            return 0
    except (GraphifyError, ValueError, OSError) as exc:
        print(f"configuration error: {exc}", file=sys.stderr)
        return 2
    return 2


if __name__ == "__main__":
    raise SystemExit(main())

