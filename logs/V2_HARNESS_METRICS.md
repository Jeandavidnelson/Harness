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
