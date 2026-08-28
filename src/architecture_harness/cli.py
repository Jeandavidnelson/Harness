from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from architecture_harness.adapters.graphify import GraphifyError, load_graphify
from architecture_harness.adapters.mermaid import MermaidError, load_mermaid_directory
from architecture_harness.adapters.rules import RulesError, load_rules
from architecture_harness.adapters.context_mermaid import load_context_directory
from architecture_harness.config import ProjectPaths
from architecture_harness.engine.harness import evaluate
from architecture_harness.exporters.json import render_json
from architecture_harness.exporters.markdown import render_markdown
from architecture_harness.exporters.text import render_text
from architecture_harness.engine.context_selector import select_context
from architecture_harness.exporters.llm_context import render_llm_context
from architecture_harness.metrics.benchmark import render_benchmark, run_benchmark
from architecture_harness.doctor import diagnose
from architecture_harness.graph_freshness import check_graph_freshness
from architecture_harness.exporters.agent_json import capabilities_payload, render_agent_context
from architecture_harness.metrics.v1_1_benchmark import render_v1_1_benchmark, run_v1_1_benchmark
from architecture_harness.ace.author import author_rule
from architecture_harness.ace.ape_adapter import validate_with_ape
from architecture_harness.graphify_runtime import GraphifyRuntimeError, refresh_graph


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="arch-harness")
    parser.add_argument("--root", type=Path, default=Path.cwd(), help="project root")
    sub = parser.add_subparsers(dest="command", required=True)
    sub.add_parser("observed", help="summarize Graphify output")
    sub.add_parser("target", help="print normalized target architecture")
    rules_parser = sub.add_parser("rules", help="validate or list rules")
    rules_parser.add_argument("action", choices=("validate", "list"))
    check = sub.add_parser("check", help="evaluate architecture policies")
    check.add_argument("--format", choices=("text", "json", "markdown"), default="text")
    context_parser = sub.add_parser("context", help="inspect or build declared context")
    context_sub = context_parser.add_subparsers(dest="context_action", required=True)
    context_sub.add_parser("overview")
    build = context_sub.add_parser("build")
    build.add_argument("--focus", action="append", required=True)
    build.add_argument("--radius", type=int, default=1)
    build.add_argument("--max-items", type=int, default=50)
    benchmark = sub.add_parser("benchmark", help="measure compact context token reduction")
    benchmark.add_argument("--tasks", type=Path)
    benchmark.add_argument("--mode", choices=("v1", "v1.1"), default="v1")
    sub.add_parser("doctor", help="validate all inputs and local cache")
    sub.add_parser("stale", help="fail when Graphify output does not match source hashes")
    graph = sub.add_parser("graph", help="manage the observed Graphify graph")
    graph_sub = graph.add_subparsers(dest="graph_action", required=True)
    graph_refresh = graph_sub.add_parser("refresh")
    graph_refresh.add_argument("--format", choices=("json",), default="json")
    agent = sub.add_parser("agent", help="stable machine-readable interface for coding agents")
    agent_sub = agent.add_subparsers(dest="agent_action", required=True)
    agent_context = agent_sub.add_parser("context")
    agent_context.add_argument("--focus", action="append", required=True)
    agent_context.add_argument("--radius", type=int, default=1)
    agent_context.add_argument("--max-items", type=int, default=50)
    agent_context.add_argument("--format", choices=("json",), default="json")
    for action in ("validate", "doctor", "capabilities"):
        command = agent_sub.add_parser(action)
        command.add_argument("--format", choices=("json",), default="json")
    ace = sub.add_parser("ace", help="experimental controlled-language authoring")
    ace_sub = ace.add_subparsers(dest="ace_action", required=True)
    ace_compile = ace_sub.add_parser("compile")
    ace_compile.add_argument("--text", required=True)
    ace_validate = ace_sub.add_parser("validate")
    ace_validate.add_argument("path", type=Path)
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
        if args.command == "check":
            result = evaluate(load_graphify(paths.observed), load_mermaid_directory(paths.target_dir), load_rules(paths.rules))
            renderer = {"text": render_text, "json": render_json, "markdown": render_markdown}[args.format]
            print(renderer(result))
            return 1 if result.violations else 0
        if args.command == "context":
            context = load_context_directory(paths.context_dir)
            if args.context_action == "overview":
                print(f"nodes: {len(context.nodes)}")
                print(f"edges: {len(context.edges)}")
                print("provenance: DECLARED_CONTEXT")
            else:
                compact = select_context(
                    args.focus, load_graphify(paths.observed), context,
                    load_mermaid_directory(paths.target_dir), load_rules(paths.rules),
                    args.radius, args.max_items,
                )
                print(render_llm_context(compact))
            return 0
        if args.command == "benchmark":
            tasks = args.tasks or paths.root / "experiments" / "tasks.yaml"
            if args.mode == "v1.1":
                print(render_v1_1_benchmark(run_v1_1_benchmark(paths, tasks)))
            else:
                print(render_benchmark(run_benchmark(paths, tasks)))
            return 0
        if args.command == "doctor":
            checks = diagnose(paths)
            for name, passed, detail in checks:
                print(f"{'PASS' if passed else 'FAIL'} {name}: {detail}")
            return 0 if all(passed for _, passed, _ in checks) else 2
        if args.command == "stale":
            freshness = check_graph_freshness(paths.root)
            print("fresh: " + ("true" if freshness.fresh else "false"))
            for path in freshness.stale_files:
                print(f"stale: {path}")
            for path in freshness.missing_files:
                print(f"missing: {path}")
            return 0 if freshness.fresh else 1
        if args.command == "graph":
            print(json.dumps(refresh_graph(paths.root), indent=2, sort_keys=True))
            return 0
        if args.command == "agent":
            if args.agent_action == "capabilities":
                print(json.dumps(capabilities_payload(), indent=2, sort_keys=True))
                return 0
            if args.agent_action == "doctor":
                checks = diagnose(paths)
                passed = all(ok for _, ok, _ in checks)
                print(json.dumps({
                    "status": "PASS" if passed else "FAIL",
                    "checks": [{"name": name, "status": "PASS" if ok else "FAIL", "detail": detail} for name, ok, detail in checks],
                }, indent=2, sort_keys=True))
                return 0 if passed else 2
            freshness = check_graph_freshness(paths.root)
            if not freshness.fresh:
                print(json.dumps({"status": "ERROR", "error": "STALE_GRAPH", "files": list(freshness.stale_files + freshness.missing_files)}, indent=2, sort_keys=True))
                return 2
            observed = load_graphify(paths.observed)
            target = load_mermaid_directory(paths.target_dir)
            rules = load_rules(paths.rules)
            if args.agent_action == "validate":
                result = evaluate(observed, target, rules)
                print(render_json(result))
                return 1 if result.violations else 0
            context = load_context_directory(paths.context_dir)
            compact = select_context(args.focus, observed, context, target, rules, args.radius, args.max_items)
            print(render_agent_context(compact))
            return 0
        if args.command == "ace":
            if args.ace_action == "compile":
                print(json.dumps(author_rule(args.text).to_dict(), indent=2, sort_keys=True))
            else:
                print(json.dumps(validate_with_ape(args.path), indent=2, sort_keys=True))
            return 0
    except (GraphifyError, GraphifyRuntimeError, MermaidError, RulesError, ValueError, OSError) as exc:
        print(f"configuration error: {exc}", file=sys.stderr)
        return 2
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
