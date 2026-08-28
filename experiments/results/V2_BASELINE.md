# V2 Baseline — V1.1 Reproduction

Date: 2026-08-28  
Source commit before V2 challenge: `0231c3d`  
V2 challenge commit: `60c470f`

## Result

**PASS — V1.1 regression baseline is reproducible.**

This result proves software regression stability. It does not prove autonomous-agent or BMAD effectiveness.

## Environment

| Item | Value |
|---|---|
| Package | architecture-harness 1.1.0 |
| Graphify | graphifyy 0.9.50 |
| Tokenizer | tiktoken:o200k_base |
| Python test runner | pytest 9.1.1 |
| Branch | feat/architecture-harness-v2 |

## Commands executed

```text
.venv/bin/pytest -q
.venv/bin/arch-harness doctor
.venv/bin/arch-harness check --format json
.venv/bin/arch-harness benchmark --mode v1.1
scripts/validate_v1_1.sh
```

## Test and gate results

| Check | Result |
|---|---|
| Unit/integration suite | 40 passed |
| Doctor | 6 checks PASS |
| Graphify freshness | PASS |
| Architecture harness | PASS, 0 violations |
| ACE focused tests | 3 passed |
| ACE skill validator | PASS |
| Full validation script | PASS |
| Combined observed wall time | 13 seconds |

## Production Graphify baseline

The validation refresh incorporated V2 challenge documents into Graphify's persistent output.

| Metric | Value |
|---|---:|
| Raw nodes | 555 |
| Normalized nodes | 569 |
| Edges | 1033 |
| EXTRACTED | 962 |
| INFERRED | 71 |
| AMBIGUOUS | 0 |
| Graph schema | NetworkX `links` |

## Existing validated rules

Eight V1.1 rules are loaded and pass:

1. `cli-must-load-observed-graph` — required edge;
2. `cli-must-run-harness` — required edge;
3. `harness-must-resolve-explicit-roles` — required edge;
4. `harness-must-support-path-evidence` — required path;
5. `doctor-must-validate-rules` — required edge;
6. `graphify-adapter-must-not-depend-on-cli` — forbidden path;
7. `token-metrics-must-not-depend-on-cli` — forbidden path;
8. `cache-must-not-call-cli` — forbidden edge.

They use nine exact role mappings. Existing tests exercise eight targeted graph mutations, but the core rule schema has no V2 status/severity/scope/provenance lifecycle yet.

## Reproduced A/B/C token metrics

| Task | A Graphify | B Graphify + full architecture | C compact context | C vs B |
|---|---:|---:|---:|---:|
| adapt Graphify schema | 4289 | 5059 | 3076 | 39.2% |
| change rule evaluation | 4425 | 5195 | 3051 | 41.3% |
| change context selection | 3776 | 4546 | 2999 | 34.0% |
| extend doctor | 4108 | 4878 | 2138 | 56.2% |
| extend agent CLI | 6444 | 7214 | 3215 | 55.4% |

Aggregate C versus B context reduction: **46.2%**.

The benchmark executes real Graphify queries, but the task implementation itself is not performed by a model. Consequently:

- model task success: `NOT_MEASURED`;
- model input/output/total tokens: `NOT_MEASURED`;
- architectural compliance after a real model implementation: `NOT_MEASURED`;
- human clarification count: `NOT_MEASURED`;
- rule maintenance cost: `NOT_MEASURED`.

## Known limitations reproduced

- a declared role may resolve zero observed nodes without producing a technical failure;
- relation type is not part of V1.1 rule evaluation;
- all loaded rules are effectively blocking and have no lifecycle;
- target Mermaid arrows are guidance and do not independently constrain observed code;
- production correction tests mutate the loaded graph in memory;
- no actual BMAD installation or workflow is tested;
- APE is unavailable and remains optional;
- Graphify output is large and changes when new repository documents are indexed;
- the branch cannot be pushed without GitHub credentials.

## Gate interpretation

Gate 1 is satisfied because the V1.1 software baseline is reproducible. V2 work may start, but it must not reuse the V1.1 benchmark as proof of agent effectiveness or use the targeted fixture rates as universal false-positive/false-negative claims.

