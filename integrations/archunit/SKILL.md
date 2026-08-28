---
name: archunit
description: Generate reviewable Java ArchUnit test candidates from Architecture Harness Mermaid context and human-validated rules while keeping native tests outside the harness core. Use when a Java project wants to enforce validated macro-architecture rules as code-level ArchUnit invariants or review existing ArchUnit coverage against harness policy.
---

# ArchUnit Test Author

Translate validated macro policy into candidate Java tests. Never generate blocking tests from Mermaid alone, inferred facts, warnings, or candidate rules.

## Workflow

1. Run `arch-harness capabilities --format json` and `arch-harness agent context --focus <java-node> --format json`.
2. Read `architecture/rules/rules.yaml`. Select only rules with `status: validated` and `provenance: USER_CONFIRMED`. Ask before translating any rule whose package mapping, scope, exceptions, or relation semantics are unclear.
3. Inspect the real Maven or Gradle build and existing test conventions. Use the project's current ArchUnit dependency/version; do not invent or silently upgrade a version.
4. Map harness roles to concrete Java packages/classes. Prefer package rules for stable boundaries and class rules only when the architecture intentionally names a concrete type.
5. Generate candidate tests in the project's test source tree with the matching test framework. Include the harness rule id and rationale in the test name or documentation.
6. Run the smallest native test command, then the project test suite when practical.
7. Run `arch-harness graph refresh --format json` and `arch-harness gate --format json` to ensure the added tests did not alter application architecture.
8. Present the diff, mapping assumptions, native test result and uncovered rules for human review. Do not weaken harness rules or application code to make a generated test pass.

## Translation guidance

- `forbidden_edge`: use a direct-dependency condition only if ArchUnit can represent the same relation; otherwise stop and explain the mismatch.
- `forbidden_path`: do not approximate transitive reachability with a direct package rule. Implement a faithful condition or leave it uncovered.
- `required_edge` and `required_path`: verify ArchUnit can observe the intended dependency type; missing dependency checks can be brittle.
- `allowed_targets` and `exceptions`: encode every validated exception explicitly and preserve its rationale.

## Safety boundary

Generated tests are candidates for human review. ArchUnit is an optional L4 code-level validator. Architecture Harness remains the L1–L3 macro gate and has no Java or ArchUnit runtime dependency.

## Completion report

Report translated rule ids, skipped rules and reasons, files changed, native test commands/results, harness gate result, and whether a human approved the generated invariant.
