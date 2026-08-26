# Architecture Harness V1

A deterministic architecture policy harness and compact task-context builder. It consumes Graphify output as trusted input, parses intentional and runtime Mermaid graphs, evaluates explicit rules, and returns bounded evidence instead of dumping complete graphs into an LLM prompt.

## Quick start

```bash
python3 -m venv .venv
.venv/bin/python -m pip install -e '.[dev]'
.venv/bin/arch-harness doctor
.venv/bin/arch-harness check
scripts/validate_v1.sh
```

`check` exits with `0` for PASS, `1` for an architecture violation, and `2` for a configuration or technical error.

## Commands

```text
arch-harness observed
arch-harness target
arch-harness rules validate
arch-harness rules list
arch-harness check --format text|json|markdown
arch-harness context overview
arch-harness context build --focus PaymentService --radius 2 --max-items 50
arch-harness benchmark
arch-harness doctor
```

Pass `--root /path/to/project` before the subcommand when running outside the project root.

## Inputs and semantics

- `graphify-out/graph.json` is consumed, never reconstructed. Nodes need `id`; edges need `source` and `target`. Relation and provenance are retained.
- `architecture/diagrams/*.mmd` describes intent. Mermaid arrows have no policy semantics by themselves.
- `architecture/rules/rules.yaml` supplies executable `required_edge`, `forbidden_edge`, `required_path`, and `forbidden_path` policies. Role matching is explicit (`exact`, `suffix`, `prefix`, or `contains`).
- `contexte/*.mmd` describes runtime/deployment/security context. Its edges remain `DECLARED_CONTEXT` and are never silently presented as observed code.
- `AMBIGUOUS` observed edges are excluded from hard failures in V1.

The supported Mermaid subset is deliberately limited to `flowchart`/`graph`, the five common directions, nodes, labels, directed edges, and subgraphs. Unsupported syntax fails as configuration error.

## CI example

```yaml
- run: python3 -m venv .venv
- run: .venv/bin/python -m pip install -e '.[dev]'
- run: scripts/validate_v1.sh
```

If Graphify is installed, `refresh_graph.sh` invokes it. Otherwise the script clearly reports that it is validating the existing trusted output. Adapt that one command to the Graphify invocation used by the target repository.

## Results

The included five-task benchmark reports a 44.0% average compact-context reduction using the documented lexical estimate (tiktoken was unavailable). The full evidence and limitations are in [V1_FINAL_REPORT.md](experiments/results/V1_FINAL_REPORT.md) and [V1_IMPLEMENTATION_LOG.md](logs/V1_IMPLEMENTATION_LOG.md).

