---
name: architecture-harness
description: Supply compact Mermaid-informed architecture context and enforce deterministic architecture checkpoints around significant code changes. Use when Claude implements, refactors, reviews, or corrects code in a project configured with Architecture Harness.
---

# Architecture Harness

1. Discover the contract with `arch-harness capabilities --format json` when needed.
2. Before significant implementation, run `arch-harness agent context --focus <relevant-node> --format json`.
3. Use declared Mermaid as guidance and validated rules as policy. Do not treat inferred facts as confirmed policy.
4. At meaningful checkpoints, run `arch-harness graph refresh --format json` then `arch-harness gate --format json`.
5. On exit 1, correct code using the reported rule, path, files, rationale and provenance; repeat refresh and gate.
6. On exit 2, run `arch-harness doctor` and repair configuration.
7. Invoke the installed `architecture-rule-author` skill automatically after Mermaid changes, after the first greenfield graph, and for unresolved mappings; do not make the user perform mapping manually.

Never edit rules merely to force PASS. The gate does not replace functional tests or code review.
