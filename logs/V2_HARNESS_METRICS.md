# V2 Harness Metrics

Metrics not supported by available instrumentation are recorded as `NOT_MEASURED`.

## Gate 0 challenge baseline

| Metric | Value |
|---|---:|
| V1.1 rules | 8 |
| Existing V1.1 tests reported | 40 passed |
| Real BMAD integration runs | 0 |
| Real autonomous correction runs | 0 |
| Human clarification count | NOT_MEASURED |
| Rule maintenance cost | NOT_MEASURED |
| Model task success | NOT_MEASURED |

## Gate 1 V1.1 regression baseline

| Metric | Value |
|---|---:|
| Tests | 40 passed |
| Doctor | PASS |
| Harness | PASS |
| Raw / normalized nodes | 555 / 569 |
| Edges | 1033 |
| EXTRACTED / INFERRED / AMBIGUOUS | 962 / 71 / 0 |
| C vs B context reduction | 46.2% |
| Full baseline wall time | 13 seconds |
| Model task success | NOT_MEASURED |
| Human clarification count | NOT_MEASURED |
| Rule maintenance cost | NOT_MEASURED |

## Gate 2 production Graphify integration

| Metric | Value |
|---|---:|
| Tests | 43 passed |
| Graph refresh | PASS |
| Freshness after refresh | PASS |
| Raw / normalized nodes | 600 / 614 |
| Edges | 1104 |
| EXTRACTED / INFERRED / AMBIGUOUS | 1031 / 73 / 0 |
| Refresh duration | 0.8931 seconds |

## Gate 3 provenance model

| Metric | Value |
|---|---:|
| Tests after graph refresh | 45 passed |
| Evidence origins supported | 6 |
| Automatic inference promotions | 0 |
| Agent validation | PASS |

## Gate 4 universal agent API

| Metric | Value |
|---|---:|
| Tests | 47 passed |
| API version | 2.0 |
| Advertised universal commands | 6 |
| Core orchestrator dependencies | 0 |
| Generic subprocess consumer | PASS |

## Gate 5 architecture gate lifecycle

| Metric | Value |
|---|---:|
| Tests | 49 passed |
| Current gate | PASS |
| Gate code mutations | 0 |
| Blocking violations | 0 |
| Exit classes | 3 |

## Gate 6 rule lifecycle

| Metric | Value |
|---|---:|
| Tests | 51 passed |
| Validated production rules | 8 |
| Candidate examples | 1 |
| Lifecycle states / severities | 5 / 3 |
| Automatic promotions | 0 |
| False blocking in lifecycle tests | 0 |

## Gate 7 rule authoring skill

| Metric | Value |
|---|---:|
| Tests | 52 passed |
| Official skill validation | PASS |
| Candidate syntax validation | PASS |
| Rules promoted | 0 |
| Real forward-test runs | 0 |
| Generalization | NOT_MEASURED |

## Gate 8 deterministic Test Lab

| Metric | Value |
|---|---:|
| Scenarios | 12 |
| Tests | 54 passed |
| Known violations detected | 4 / 4 |
| Detection rate | 100% |
| False blocking rate | 0% |
| Real agent runs | 0 |
| Initial scenario-model defects found | 1 |

## Gate 9 real agent correction

| Metric | Value |
|---|---:|
| Real Codex processes | 2 |
| First-pass full task success | 0 / 1 |
| Final runtime + gate success | 1 / 1 |
| Correction iterations | 2 |
| Rule-model defects discovered | 1 |
| Input tokens (cached included separately) | 433672 |
| Cached input tokens | 380416 |
| Output tokens | 4563 |

## Gate 10 BMAD adapter

| Metric | Value |
|---|---:|
| Tests | 57 passed |
| BMAD version inspected | 6.11.0 |
| BMAD Codex skills rendered | 49 |
| Official overrides resolved | 3 / 3 |
| Core BMAD dependencies | 0 |
| Silent overwrites | 0 |
| BMAD build runtime | BLOCKED_BY_MISSING_UV |

## Gate 11 BMAD E2E

| Metric | Value |
|---|---:|
| Real BMAD workflow runs | 1 |
| uv version | 0.12.7 |
| Compact context tokens | 490 |
| BMAD spec tokens | 798 |
| FAIL propagation | PASS |
| Post-approval correction | NOT_RUN |
| E2E status | PARTIAL_HUMAN_APPROVAL_REQUIRED |

## Gate 12 portability

| Metric | Value |
|---|---:|
| Tests | 59 passed |
| Adapters sharing V2 CLI | 4 |
| Core orchestrator imports | 0 |
| Generic subprocess | PASS |
| Codex real execution | PASS_WITH_QUALIFICATIONS |
| Claude real execution | NOT_MEASURED |
