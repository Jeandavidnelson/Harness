# Architecture Harness Agent Instructions

Before significant code changes:

1. Run `arch-harness agent context --focus <relevant-node> --format json` and use the returned compact context instead of loading the full graph.
2. Make the requested change.
3. Run `scripts/refresh_graph.sh` (adapt its Graphify invocation for this repository if needed).
4. Run `arch-harness agent validate --format json`.
5. If it fails, fix all architecture violations before completion.

For changes to the harness itself, run `scripts/validate_v1_1.sh`. Preserve observed versus declared provenance and keep policy evaluation deterministic; do not add LLM inference to the policy engine. Exit code 1 means architecture violations; exit code 2 means a technical/configuration problem and should be diagnosed with `arch-harness agent doctor --format json`.
