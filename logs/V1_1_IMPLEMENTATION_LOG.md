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
