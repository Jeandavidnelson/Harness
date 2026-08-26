# V1 Final Report

Date: 2026-08-26

## Decision

**GO** for the V1 architecture harness and compact-context workflow. The harness meets every P0 fixture criterion, the measured context reduction exceeds 30%, and reports contain enough evidence for the tested one-iteration correction loop.

## Functional evidence

- 15 tests pass.
- Direct and indirect forbidden dependencies are detected.
- Missing required edges and paths are detected.
- An unrelated extra `Service -> Logger` dependency remains PASS.
- `AMBIGUOUS` evidence does not cause a hard failure.
- PASS → FAIL → PASS is covered by a regression test.
- `doctor` validates all inputs, explicit mappings, and cache access.
- `validate_v1.sh` completed the refresh/validate/test/check/benchmark sequence.

No false positive or false negative was observed in the defined V1 fixtures. This statement is limited to those fixtures, not arbitrary Mermaid or Graphify dialects.

## Token benchmark

All rows use the same useful raw input and deterministic lexical estimator because the target tokenizer was unavailable.

| Task | Raw context | Graph query | V1 context | Reduction |
|---|---:|---:|---:|---:|
| Modify PaymentService | 493 | 327 | 312 | 36.7% |
| Repository change impact | 493 | 327 | 270 | 45.2% |
| Add external service | 493 | 327 | 258 | 47.7% |
| Refactor Controller | 493 | 327 | 270 | 45.2% |
| Simple architecture violation | 493 | 327 | 270 | 45.2% |
| **Mean** | **493** | **327** | **276** | **44.0%** |

No measured task costs more than its raw baseline. The PaymentService task saves less because radius-one selection legitimately includes all of its observed neighbors and connected declared infrastructure.

## A/B/C comparison

| Metric | A — Graphify + manual read | B — Graphify + full architecture | C — V1 compact + harness |
|---|---:|---:|---:|
| Context tokens | Not separately measured | 493 raw / 327 projected | 258–312 |
| Deterministic policy result | No | No | Yes |
| Violations in scenario | Agent-dependent | Agent-dependent | 1 detected, then 0 |
| Correction iterations | Not measured | Not measured | 1 |
| Success | Not measured | Not measured | Yes |
| Tool calls / files read / time | Not measured | Not measured | Automated, time not retained |

Unmeasured values are kept explicit rather than invented. The reproducible benchmark measures context size, while the integration fixture measures correction behavior.

## Assessment

- Harness detection: PASS for 100% of required P0 fixtures.
- False positives: none in the allow/extra-dependency fixture.
- Feedback quality: sufficient to identify the rule, shortest observed path, relevant files, and provenance without a full graph reload.
- CI readiness: yes; stable exit codes and `validate_v1.sh` are available.
- Token utility: PASS; 44.0% mean reduction, above the 30% success threshold.
- Quality caveat: V1 matching is lexical and explicit. It does not infer architecture roles.

## Limits and next gate

Before wider adoption, connect `refresh_graph.sh` to the exact Graphify CLI used by the target codebase and rerun with a real production fixture and the target model tokenizer. ACE, APE, CNL, NLP compilation, vector search, MCP, and multi-agent orchestration remain intentionally out of scope.

