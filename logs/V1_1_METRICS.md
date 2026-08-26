# V1.1 Metrics

Unknown metrics are recorded as `NOT_MEASURED`.

## Graphify production baseline — 2026-08-26

| Metric | Value |
|---|---:|
| Graphify version | 0.9.50 |
| Raw nodes | 143 |
| Normalized nodes | 152 |
| Edges | 497 |
| EXTRACTED edges | 497 |
| INFERRED edges | 0 |
| AMBIGUOUS edges | 0 |
| Graphify calls during integration | 3 |
| Duration | NOT_MEASURED |

## Gate 1 final refresh

| Metric | Value |
|---|---:|
| Raw nodes | 298 |
| Normalized nodes | 307 |
| Edges | 665 |
| EXTRACTED | 600 |
| INFERRED | 65 |
| AMBIGUOUS | 0 |
| Stale cycles validated | 1 complete add/remove cycle |
| Tests | 19 passed |

## Real A/B/C context benchmark

| Task | A Graphify | B Graphify + full architecture | C agent context | C vs B |
|---|---:|---:|---:|---:|
| adapt-graphify-schema | 3468 | 3753 | 2498 | 33.4% |
| change-rule-evaluation | 3590 | 3875 | 2503 | 35.4% |
| change-context-selection | 3271 | 3556 | 2501 | 29.7% |
| extend-doctor | 3623 | 3908 | 1576 | 59.7% |
| extend-agent-cli | 5325 | 5610 | 2566 | 54.3% |
| **Mean** | **3855.4** | **4140.4** | **2328.8** | **43.8%** |

- C vs A mean reduction: 39.6%.
- Tokenizer: `tiktoken:o200k_base`.
- Model task success, input/output/total model tokens: `NOT_MEASURED`.
- Each A/B row executes one real Graphify query. C uses the refreshed graph and deterministic selector.

## Real policy corpus

| Metric | Value |
|---|---:|
| Rules | 8 |
| Exact role mappings | 9 |
| Baseline violations | 0 |
| Injected regressions | 8 |
| Detected regressions | 8 |
| False positives | 0 |
| False negatives | 0 |
| Detection duration | NOT_MEASURED |

## Agent correction loops

| Scenario | Initial context tokens | Feedback tokens | Iterations | Final result |
|---|---:|---:|---:|---|
| Missing CLI -> harness edge | 3143 | 107 | 1 | PASS |
| Graphify adapter -> CLI forbidden edge | 3024 | 167 | 1 | PASS |
| Token metrics -> bridge -> CLI forbidden path | 1216 | 163 | 1 | PASS |

Full graph baseline: 114604 `o200k_base` tokens. Model tool calls and model file reads are `NOT_MEASURED`.

## ACE/CNL experiment

| Metric | Value |
|---|---:|
| Corpus cases | 7 |
| Exact cases stable | 4/4 |
| Ambiguous cases requiring clarification | 3/3 |
| Ambiguous cases hardened | 0 |
| Unsupported cases in corpus | 0 |
| Skill validator | PASS on iteration 2 |
| APE | UNAVAILABLE / NOT_RUN |

## Final global-validation benchmark

The repository grew during V1.1, so the final reproducible run supersedes—but does not erase—the earlier Gate 4 snapshot.

| Metric | Value |
|---|---:|
| Mean A context | 4608.4 tokens |
| Mean B context | 5378.4 tokens |
| Mean C context | 2895.8 tokens |
| C vs B reduction | 46.2% |
| C vs A reduction | 37.2% |
| Full tests | 40 passed |
| ACE focused tests | 3 passed |
| Harness | PASS |
| Skill validator | PASS |
