# Architecture-aware development workflow

```text
context
  arch-harness agent context --focus {{focus_node}} --format json
dev
  implement the scoped task using relevant_files and applicable_rules
refresh
  arch-harness graph refresh --format json
validate
  arch-harness gate --format json
correct
  on exit 1, fix every reported violation and repeat refresh + validate
diagnose
  on exit 2, run arch-harness agent doctor --format json
```

Never substitute declared Mermaid context for observed Graphify evidence. Never ask an LLM to decide PASS/FAIL.
