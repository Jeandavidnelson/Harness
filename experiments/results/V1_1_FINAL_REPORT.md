# V1.1 Final Report

Date: 2026-08-26

## Decision

**GO HARNESS + CONTEXT + ACE EXPERIMENT**

The deterministic harness and compact context workflow meet their gates on the real repository. ACE is accepted only as an experimental authoring layer. It does not replace `rules.yaml` or decide PASS/FAIL.

## Graphify integration

- Official `graphifyy==0.9.50` installed in the project environment.
- Real refresh: `graphify update . --no-cluster`.
- Final normalized graph: 522 nodes, 992 edges after the documentation refresh.
- Official `edges` and NetworkX `links` schemas supported.
- `confidence`/`provenance` and `source_file`/`file` aliases normalized.
- A stale fixture semantic layer was discovered and removed by a clean rebuild.
- A real temporary import dependency proved stale detection, refresh visibility, fix detection and post-fix disappearance.

## Harness

- Eight rules over real Graphify IDs.
- Nine exact role mappings.
- Baseline: PASS.
- Injected regressions detected: 8/8.
- False positives in defined corpus: 0.
- False negatives in defined corpus: 0.
- Final full test gate before documentation: 40 passed.

These figures apply to the defined corpus and do not claim universal static-analysis completeness.

## Context and tokens

Final global-run means using `tiktoken:o200k_base`:

| Condition | Mean context tokens |
|---|---:|
| A — Graphify query | 4608.4 |
| B — Graphify + full architecture | 5378.4 |
| C — universal agent context | 2895.8 |

- C versus B reduction: 46.2%.
- C versus A reduction: 37.2%.
- C retains deterministic harness PASS in every benchmark row.
- Model task success, output tokens and total model tokens: `NOT_MEASURED`.

## Agent portability

- Universal JSON commands: context, validate, doctor, capabilities.
- Claude adapter: PASS.
- Codex instructions: PASS.
- BMAD workflow: PASS.
- Adapters contain no policy-engine business logic.
- Stale graphs are rejected before agent context or validation.

## Correction loops

Three production-graph scenarios passed in one correction iteration each:

| Scenario | Feedback tokens | Final result |
|---|---:|---|
| Missing required CLI/harness edge | 107 | PASS |
| Forbidden Graphify-adapter/CLI edge | 167 | PASS |
| Forbidden token-metrics/CLI path | 163 | PASS |

Full graph comparison: 114604 tokens.

## ACE experiment

- Reusable skill created and validated by the official skill validator.
- Corpus: four exact cases and three ambiguous cases.
- Exact stability: 4/4.
- Ambiguities hardened silently: 0.
- APE: `UNAVAILABLE / NOT_RUN`; harness unaffected.
- ALLOW statements remain authoring output when no standalone deterministic V1.1 mapping exists.

## Version control

- V1 baseline tagged locally as `v1.0.0` on commit `d4840d1`.
- V1.1 developed on `feat/architecture-harness-v1_1` with gated commits.
- Push attempts failed because GitHub credentials were unavailable in the execution environment. No successful remote push is claimed.

## Remaining evidence gap

A controlled external model runner was unavailable. Therefore model task-success non-degradation, model output tokens and total model tokens remain unmeasured. This prevents a stronger claim about all downstream LLM quality, but does not invalidate the deterministic harness, stale protection, context-size measurements, or correction fixtures.
