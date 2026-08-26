# V1.1 Implementation Log

Dates use Europe/Paris. Negative and unavailable results are retained.

## Gate 0 — Versioning and inspection — 2026-08-26

### Objectif
Preserve V1.0.0 and inspect the real V1 baseline.

### Hypothèse
The current commit is a reproducible V1 baseline and the remote accepts the requested tag.

### Commit
V1 baseline `d4840d1`; annotated local tag `v1.0.0`.

### Configuration
Branch `feat/architecture-harness-v1_1`, remote `origin` over HTTPS.

### Commandes
`git tag -a v1.0.0 ...`, `git push origin v1.0.0`, repository inspection.

### Tests et métriques
- local tag: PASS
- remote tag push: FAIL — GitHub credentials unavailable
- files read: 2 external specifications plus repository inspection
- duration: NOT_MEASURED
- final production graph: 298 raw nodes / 665 edges; 307 normalized nodes
- pytest: 19 passed
- stale dependency cycle: stale detected -> import edge present after refresh -> stale detected after fix -> edge absent after refresh
- harness result: PASS

### Résultat
The exact V1 commit is tagged locally. Push failure was not hidden.

### Statut
PARTIAL because remote authentication is unavailable.

## Gate 1 — Production Graphify integration — 2026-08-26

### Objectif
Replace the illustrative graph with a real deterministic Graphify AST extraction and reject stale output.

### Hypothèse
Graphify can extract this Python repository locally without an LLM.

### Commit
Pending after validation.

### Configuration
`graphifyy==0.9.50`, `graphify extract . --code-only --no-cluster`, incremental `graphify update . --no-cluster`.

### Commandes
Install Graphify, perform a clean extraction, run `observed`, `check`, stale checks and pytest.

### Tests et métriques
- first incremental extraction: 148 nodes / 501 edges, but retained 9 stale semantic fixture nodes — FAIL
- clean extraction: 143 raw nodes / 497 edges, AST-only — PASS
- normalized graph: 152 nodes / 497 edges (dangling edge endpoints normalized as nodes)
- Graphify calls: 3
- stale fixture output backup: `/tmp/harness-graphify-v1.7G5cfW/graphify-out`
- duration: NOT_MEASURED

### Problèmes
The V1 fixture was silently preserved as a semantic baseline. The adapter also needed official `confidence` and `source_file` aliases.

### Corrections
Rebuilt from an empty output directory, added official schema aliases, real refresh command, manifest hash validation, and missing-source detection.

### Statut
PASS

## Gate 4 — Real A/B/C context benchmark — 2026-08-26

### Objectif
Compare real Graphify query output, Graphify plus full architecture, and universal agent context on five repository tasks.

### Hypothèse
Condition C reduces context versus B without removing harness validation.

### Commit
Pending after validation.

### Configuration
Graphify CLI queries, `tiktoken:o200k_base`, identical repository and task focuses.

### Commandes
`arch-harness benchmark --mode v1.1`, pytest.

### Tests et métriques
- pytest: 24 passed
- tasks: 5 real repository focuses
- A mean context: 3855.4 tokens
- B mean context: 4140.4 tokens
- C mean context: 2328.8 tokens
- C vs B reduction: 43.8%
- C vs A reduction: 39.6%
- tokenizer: `tiktoken:o200k_base`
- task success/output tokens/total tokens: NOT_MEASURED

### Résultat
Condition C reduces context on every task versus B and retains a deterministic PASS result.

### Problèmes et corrections
Model output/total tokens and task success are not available without a model task runner; they remain `NOT_MEASURED`.

### Statut
PASS for context reduction; task-success non-degradation remains NOT_MEASURED.

## Gate 3 — Agent adapters — 2026-08-26

### Objectif
Provide thin Claude, Codex and BMAD instructions over the same JSON contract.

### Hypothèse
Documentation-only adapters are sufficient when the engine API is stable.

### Commit
Pending after validation.

### Configuration
Workflow: context -> dev -> refresh -> validate -> correct.

### Commandes
Adapter consistency tests and full pytest.

### Tests et métriques
- pytest: 23 passed
- adapters: 3 (Claude, Codex, BMAD)
- engine policy code added by adapters: 0

### Résultat
All adapters call the same context and validate commands and preserve provenance guidance.

### Problèmes et corrections
None known.

### Statut
PASS

## Gate 2 — Universal agent JSON contract — 2026-08-26

### Objectif
Expose stable bounded JSON commands for context, validation, diagnostics and capability discovery.

### Hypothèse
All agents can integrate through process execution and JSON without harness-specific business logic.

### Commit
Pending after validation.

### Configuration
API version 1.1; JSON only; exit codes 0/1/2; stale graph rejected before context or validation.

### Commandes
`arch-harness agent context|validate|doctor|capabilities --format json`.

### Tests et métriques
- pytest: 22 passed
- commands: 4/4 return parseable JSON
- sample context: 44 observed edges, 7 files, 1629 lexical-estimate tokens
- full graph dump in agent context: absent
- stale graph rejection: implemented before context/validate

### Résultat
All four universal commands satisfy the bounded JSON contract.

### Problèmes et corrections
The focus currently has no connected declared Mermaid nodes; the empty declared-context array is explicit rather than fabricated.

### Statut
PASS
