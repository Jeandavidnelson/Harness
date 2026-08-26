# Architecture Harness Agent Instructions

Before significant code changes:

1. Run `arch-harness context build --focus <relevant-node>` and use the returned compact context instead of loading the full graph.
2. Make the requested change.
3. Run `scripts/refresh_graph.sh` (adapt its Graphify invocation for this repository if needed).
4. Run `arch-harness check`.
5. If it fails, fix all architecture violations before completion.

For changes to the harness itself, run `scripts/validate_v1.sh`. Preserve observed versus declared provenance and keep policy evaluation deterministic; do not add LLM inference to V1.

