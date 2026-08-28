# Architecture Harness

Use this skill before and after significant code changes in this repository.

## Workflow

1. Request bounded context:
   `arch-harness agent context --focus <node> --format json`
2. Modify only the relevant code.
3. Refresh observed architecture:
   `arch-harness graph refresh --format json`
4. Validate:
   `arch-harness gate --format json`
5. When validation returns exit code 1, use each compact violation's rule, path, files and provenance to correct the code, then repeat steps 3–4.
6. When Mermaid changes, after the first greenfield graph, or when a mapping is unresolved, invoke `/architecture-rule-author` automatically with `arch-harness rules author-context --format json`. Ask the user only about remaining ambiguity or promotion.

Run `arch-harness agent doctor --format json` when a command returns exit code 2. Do not infer missing architectural rules, treat declared context as observed code, or dump `graphify-out/graph.json` into the model context.
