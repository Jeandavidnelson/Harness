# Architecture Harness

Use this skill before and after significant code changes in this repository.

## Workflow

1. Request bounded context:
   `arch-harness agent context --focus <node> --format json`
2. Modify only the relevant code.
3. Refresh observed architecture:
   `scripts/refresh_graph.sh`
4. Validate:
   `arch-harness agent validate --format json`
5. When validation returns exit code 1, use each compact violation's rule, path, files and provenance to correct the code, then repeat steps 3–4.

Run `arch-harness agent doctor --format json` when a command returns exit code 2. Do not infer missing architectural rules, treat declared context as observed code, or dump `graphify-out/graph.json` into the model context.

