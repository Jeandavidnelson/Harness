# V1 Implementation Log

Negative results are retained. Dates use the repository's local date.

## Étape 1 — 2026-08-26

### Objectif
Consume Graphify JSON directly as a normalized `ObservedGraphIR`.

### Commit
Pending at test time; recorded in Git history after validation.

### Fichiers créés / modifiés
`pyproject.toml`, Graphify adapter and IR, sample graph and unit fixture.

### Commandes exécutées
`arch-harness observed`, `pytest`, `git status`, `git diff`.

### Tests
Adapter normalization and provenance summary.

### Résultat fonctionnel
The adapter consumes nodes and edges without rebuilding Graphify.

### Problèmes rencontrés
The initial workspace was empty and had no Python test dependencies.

### Corrections effectuées
Created a standard `src` package; dependency installation is isolated to development.

### Métriques
- tests passés: 2
- erreurs: 0 known
- token benchmark: N/A
- contexte brut: N/A
- contexte optimisé: N/A

### Statut
PASS

## Étapes 4–5 — 2026-08-26

### Objectif
Evaluate architecture deterministically and emit compact agent-friendly reports.

### Commit
Pending at test time; recorded in Git history after validation.

### Fichiers créés / modifiés
Path search, harness, violation model, exporters, CLI and regression scenarios.

### Commandes exécutées
`arch-harness check` in text/JSON/Markdown, `pytest`.

### Tests
PASS, direct and indirect violation, missing dependency, allowed extra edge, ambiguous provenance.

### Résultat fonctionnel
Exit 0 means PASS, 1 means policy violation and 2 means technical/configuration failure.

### Problèmes rencontrés
Default example initially conflicted with its intended external-client dependency.

### Corrections effectuées
Changed the forbidden-path example to Domain/Infrastructure roles and retained external-client flow as intended architecture.

### Métriques
- tests passés: 10
- erreurs: 0 known
- token benchmark: N/A
- contexte brut: N/A
- contexte optimisé: N/A

### Statut
PASS

## Étape 3 — 2026-08-26

### Objectif
Load and validate executable V1 rules with explicit role mappings.

### Commit
Pending at test time; recorded in Git history after validation.

### Fichiers créés / modifiés
Rules IR/adapter, matcher, sample policy, CLI and tests.

### Commandes exécutées
`arch-harness rules validate`, `arch-harness rules list`, `pytest`.

### Tests
Rule parsing, allowlist parsing and deterministic suffix role matching.

### Résultat fonctionnel
All four required rule types validate; mappings contain no LLM inference.

### Problèmes rencontrés
No YAML library existed in the empty workspace.

### Corrections effectuées
Implemented only the deliberately constrained V1 YAML subset, rejecting unsupported syntax.

### Métriques
- tests passés: 4
- erreurs: 0 known
- token benchmark: N/A
- contexte brut: N/A
- contexte optimisé: N/A

### Statut
PASS

## Étape 2 — 2026-08-26

### Objectif
Parse intentional Mermaid architecture into normalized nodes, edges, labels and subgraphs.

### Commit
Pending at test time; recorded in Git history after validation.

### Fichiers créés / modifiés
Mermaid adapter, architecture IR, target diagrams, CLI and tests.

### Commandes exécutées
`arch-harness target`, `pytest`, `git status`, `git diff`.

### Tests
Flowchart edges, labels and subgraph membership.

### Résultat fonctionnel
Target diagrams are parsed without assigning policy semantics to their arrows.

### Problèmes rencontrés
None.

### Corrections effectuées
N/A.

### Métriques
- tests passés: 3
- erreurs: 0 known
- token benchmark: N/A
- contexte brut: N/A
- contexte optimisé: N/A

### Statut
PASS
