# V2 A/B/C Benchmark

Date: 2026-08-28  
Tasks: 5 identical focus tasks  
Tokenizer: tiktoken `o200k_base`

## Conditions

- A: production Graphify query only.
- B: production Graphify query plus all architecture/context/rule files.
- C: Architecture Harness compact context derived from the existing observed graph.

This run benchmarks context assembly, not model implementation. Task success and model output metrics remain `NOT_MEASURED` for all fifteen rows.

| Task | A tokens | B tokens | C tokens | C vs B |
|---|---:|---:|---:|---:|
| adapt Graphify schema | 6249 | 7163 | 3493 | 51.2% |
| change rule evaluation | 5075 | 5989 | 3520 | 41.2% |
| change context selection | 4270 | 5184 | 3434 | 33.8% |
| extend doctor | 4579 | 5493 | 2447 | 55.5% |
| extend agent CLI | 7620 | 8534 | 3694 | 56.7% |

Aggregate C-versus-B context reduction: **48.7%**.

Condition C context construction took 0.0044–0.0047 seconds per task and made no additional Graphify call. Conditions A and B each made one real Graphify query per task. B read seven inputs; C selected 8–26 relevant files depending on graph connectivity.

## Required metrics

| Metric | Result |
|---|---|
| Task success | NOT_MEASURED |
| Architectural compliance after model work | NOT_MEASURED |
| Violations introduced | NOT_MEASURED |
| Violations detected | NOT_MEASURED in A/B/C model tasks; deterministic Test Lab measured separately |
| False positives / false negatives | NOT_MEASURED for model tasks |
| Correction iterations | NOT_MEASURED for these five tasks |
| Tool calls | 1 per context condition |
| Graphify calls | A=5, B=5, C=0 |
| Input/context tokens | MEASURED above |
| Output/total model tokens | NOT_MEASURED |
| Human clarification count | NOT_MEASURED |
| Rule maintenance cost | NOT_MEASURED |

## Interpretation

C reduces architecture context compared with B, but it is not uniformly smaller by the same margin and selected file count is not equivalent to files physically read by a model. The benchmark does not establish that compact context improves task success. Gate 9 provides one separate real-agent correction observation and cannot support a five-task success rate.
