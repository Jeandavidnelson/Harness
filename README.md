# Architecture Harness V1.1

Architecture Harness est un logiciel Python qui transforme une architecture logicielle souhaitée en contrôles automatiques, reproductibles et exploitables par des humains comme par des agents de développement.

Il combine quatre sources d’information sans les confondre :

1. le graphe du code réellement observé par Graphify ;
2. l’architecture cible déclarée en Mermaid ;
3. les règles exécutables déclarées explicitement ;
4. le contexte d’exécution externe au code, également déclaré en Mermaid.

Le résultat est un harness déterministe qui retourne `PASS` ou `FAIL`, accompagné d’une preuve compacte. Le même graphe sert aussi à construire un contexte ciblé afin qu’un agent n’ait pas à charger tout le repository dans son prompt.

## Pourquoi ce logiciel existe

Un diagramme d’architecture classique documente une intention, mais il ne garantit pas que le code la respecte. À l’inverse, un graphe extrait du code décrit ce qui existe, mais ne sait pas à lui seul ce qui est autorisé ou interdit.

Architecture Harness relie ces deux mondes :

```text
Code source
   │
   ▼
Graphify ───────────────► graphe observé
                              │
Mermaid cible ────────────────┤
Règles explicites ────────────┤──► harness ──► PASS / FAIL + preuve
                              │
Mermaid de contexte ──────────┘
                              │
                              └──► sélecteur ──► contexte agent compact
```

Le LLM n’est jamais chargé de calculer les chemins, de trouver les violations ou de décider du résultat. Ces opérations sont exécutées par du code Python. Un modèle peut proposer une modification ou aider à écrire une règle, mais le verdict reste produit par le moteur déterministe.

## Principes fondamentaux

### 1. Séparer observation, intention et politique

- `graphify-out/graph.json` contient l’observation du code.
- `architecture/diagrams/*.mmd` décrit l’intention architecturale.
- `architecture/rules/rules.yaml` définit la politique exécutable.
- `contexte/*.mmd` décrit ce que le code seul ne montre pas : processus externes, infrastructure, frontières de confiance ou déploiement.

Une flèche Mermaid `A --> B` ne signifie pas automatiquement « A doit appeler B ». Elle décrit seulement la cible. La sémantique obligatoire ou interdite vient toujours de `rules.yaml`.

### 2. Conserver la provenance

Chaque relation garde son origine :

- `EXTRACTED` : relation directement extraite du code ;
- `INFERRED` : relation résolue par Graphify ;
- `AMBIGUOUS` : relation incertaine, ignorée pour les échecs durs en V1.1 ;
- `DECLARED_CONTEXT` : relation déclarée dans un Mermaid de contexte.

Une relation déclarée n’est jamais présentée silencieusement comme une observation du code.

### 3. Préférer les règles explicites

Les rôles sont associés au code par des matchers déclarés : `exact`, `suffix`, `prefix` ou `contains`. Il n’existe aucune inférence LLM de rôle dans le harness.

Les quatre règles disponibles sont :

| Type | Signification |
|---|---|
| `required_edge` | une dépendance directe doit exister |
| `forbidden_edge` | une dépendance directe ne doit pas exister |
| `required_path` | un chemin direct ou transitif doit exister |
| `forbidden_path` | aucun chemin direct ou transitif ne doit exister |

### 4. Refuser les graphes périmés

Graphify maintient `graphify-out/manifest.json` avec le hash des sources analysées. La commande `arch-harness stale` compare ces hashes aux fichiers Python, shell et au manifeste du package.

Si une source change sans refresh, les commandes agent `context` et `validate` refusent de continuer avec le code d’erreur technique `2`. Le système ne donne donc pas un faux sentiment de sécurité à partir d’un ancien graphe.

### 5. Borner le contexte agent

Le sélecteur part d’un nœud focus, explore ses voisins dans un rayon borné, conserve les chemins utiles, projette les règles applicables et liste les fichiers pertinents. Les limites portent d’abord sur la structure — rayon et nombre d’éléments — puis les tokens sont mesurés.

Le graphe complet n’est jamais renvoyé par défaut dans l’interface agent.

## Architecture interne

```text
src/architecture_harness/
├── adapters/       lecture Graphify, Mermaid et règles
├── ir/             représentations intermédiaires normalisées
├── engine/         matching, chemins, harness et sélection de contexte
├── exporters/      sorties text, Markdown, JSON et JSON agent
├── metrics/        tokenisation et benchmarks A/B/C
├── cache/          cache local adressé par contenu
├── ace/            expérimentation d’authoring ACE, séparée du harness
├── graph_freshness.py
├── doctor.py
└── cli.py
```

### Flux de validation

1. L’adapter Graphify normalise les variantes officielles `edges` et `links`, ainsi que `provenance`/`confidence` et `file`/`source_file`.
2. Le parser Mermaid transforme les diagrammes en nœuds, arêtes et appartenances aux subgraphs.
3. Le parser de règles charge le sous-ensemble YAML volontairement limité de la V1.1.
4. Le matcher résout chaque rôle vers des identifiants Graphify exacts.
5. Le moteur cherche les arêtes ou chemins requis/interdits.
6. Pour un chemin interdit, le plus court chemin observé devient la preuve.
7. Les exporters limitent le rapport aux violations, fichiers et provenances nécessaires.

## Installation

Prérequis : Python 3.10 ou supérieur.

```bash
python3 -m venv .venv
.venv/bin/python -m pip install -e '.[dev]'
.venv/bin/arch-harness doctor
```

Les dépendances de développement installent Graphify `0.9.50`, pytest, `tiktoken` et les outils nécessaires à la validation du Skill ACE.

## Workflow quotidien détaillé

### Étape 1 — Construire le contexte avant de modifier le code

```bash
.venv/bin/arch-harness agent context \
  --focus src_architecture_harness_engine_harness_evaluate \
  --format json
```

La réponse contient uniquement :

- les arêtes observées pertinentes ;
- le contexte Mermaid connecté ;
- la projection de l’architecture cible ;
- les règles applicables ;
- les fichiers pertinents ;
- les provenances ;
- les métriques et l’indication de troncature.

Le focus accepte aussi une sous-chaîne pratique telle que `evaluate` ou `load_graphify`.

### Étape 2 — Modifier les fichiers pertinents

La modification s’effectue normalement. Le harness n’impose aucun framework et ne remplace ni Git, ni les tests métier, ni Graphify.

### Étape 3 — Rafraîchir l’observation

```bash
scripts/refresh_graph.sh
```

Le script exécute réellement le binaire Graphify de `.venv`. Si un manifest existe, il effectue une mise à jour incrémentale ; sinon il effectue une extraction AST locale complète en mode code-only. Il vérifie ensuite immédiatement la fraîcheur du résultat et affiche le résumé du graphe.

Pour lancer Graphify directement :

```bash
.venv/bin/graphify extract . --code-only --no-cluster
.venv/bin/graphify update . --no-cluster
```

Graphify est utilisé comme moteur d’observation éprouvé ; Architecture Harness ne réimplémente pas son analyse AST. Voir la [documentation Graphify](https://graphify.com/docs) et le [repository officiel](https://github.com/Graphify-Labs/graphify).

### Étape 4 — Valider l’architecture

Pour un humain :

```bash
.venv/bin/arch-harness check --format text
.venv/bin/arch-harness check --format markdown
.venv/bin/arch-harness check --format json
```

Pour un agent :

```bash
.venv/bin/arch-harness agent validate --format json
```

Codes de sortie :

| Code | Signification | Action |
|---:|---|---|
| `0` | architecture conforme | terminer ou poursuivre les tests métier |
| `1` | violation architecturale | corriger toutes les violations puis rafraîchir |
| `2` | erreur technique/configuration | lancer `agent doctor` et corriger la configuration |

### Étape 5 — Corriger une violation

Le rapport compact fournit :

- l’identifiant de règle ;
- le type de politique ;
- la source et la cible ;
- le plus court chemin observé ;
- les fichiers concernés ;
- la provenance des relations.

L’agent corrige le code à partir de cette preuve, rejoue `refresh_graph.sh`, puis `agent validate`. Les trois scénarios V1.1 ont demandé une seule itération, avec des feedbacks de 107 à 167 tokens contre 114 604 tokens pour le graphe complet.

## Interface universelle pour agents

```bash
arch-harness agent capabilities --format json
arch-harness agent doctor --format json
arch-harness agent context --focus <node> --format json
arch-harness agent validate --format json
```

Les adapters n’ajoutent aucune logique métier :

- Codex : `AGENTS.md` ;
- Claude : `integrations/claude/architecture-harness/SKILL.md` ;
- BMAD : `integrations/bmad/workflow-snippet.md`.

Un nouvel agent peut découvrir le contrat via `capabilities`, diagnostiquer l’installation, demander son contexte, modifier le code et consommer le résultat de validation sans connaître l’implémentation interne.

## Écrire une règle

Exemple de règle réelle :

```yaml
roles:
  CliMain:
    match:
      exact: src_architecture_harness_cli_main
  HarnessEvaluate:
    match:
      exact: src_architecture_harness_engine_harness_evaluate

rules:
  - id: cli-must-run-harness
    type: required_edge
    source: CliMain
    target: HarnessEvaluate
```

Workflow recommandé :

1. trouver les identifiants réels avec Graphify ;
2. ajouter un matcher explicite ;
3. choisir edge ou path selon la sémantique directe ou transitive ;
4. exécuter `arch-harness rules validate` ;
5. exécuter `scripts/refresh_graph.sh` si du code a changé ;
6. exécuter `arch-harness check` ;
7. ajouter un test PASS et un test de régression FAIL.

## Expérimentation ACE/CNL

ACE est une couche d’aide à l’écriture, pas le harness.

```bash
arch-harness ace compile \
  --text "Controllers must never call repositories directly."
```

La sortie conserve l’original, l’intention, le statut, le candidat ACE, l’interprétation structurée, les hypothèses et un mapping harness éventuel.

Les statuts sont :

- `EXACT` : la modalité et la relation sont suffisamment précises ;
- `NEEDS_CLARIFICATION` : la phrase contient par exemple `should`, `normally`, `preferably` ou une condition inexécutable ;
- `UNSUPPORTED` : la relation dépasse le corpus déterministe ou combine plusieurs contraintes.

Une formulation comme « Services should use caching when useful » ne devient jamais une obligation. Elle retourne `NEEDS_CLARIFICATION`, sans ACE et sans règle harness.

Validation APE optionnelle :

```bash
arch-harness ace validate rule.ace
```

Lorsque l’exécutable APE n’est pas installé, la commande retourne `UNAVAILABLE / NOT_RUN` sans casser le harness principal.

Le skill réutilisable se trouve dans `integrations/ace-rule-author/`.

## Validation complète et CI

La commande de référence est :

```bash
scripts/validate_v1_1.sh
```

Elle exécute, dans cet ordre :

1. refresh Graphify ;
2. stale graph check ;
3. doctor JSON ;
4. suite pytest complète ;
5. harness ;
6. benchmark A/B/C ;
7. tests ACE ;
8. validation structurelle du skill ;
9. ajout du résumé au journal.

Exemple CI :

```yaml
- run: python3 -m venv .venv
- run: .venv/bin/python -m pip install -e '.[dev]'
- run: scripts/validate_v1_1.sh
```

## Benchmark V1.1

Les cinq tâches portent sur des nœuds réels du repository. Les tokens sont mesurés avec `tiktoken:o200k_base`.

| Condition | Contenu |
|---|---|
| A | sortie d’une vraie requête Graphify |
| B | Graphify + architecture et contexte complets |
| C | `arch-harness agent context` |

Résultat final :

- moyenne A : 4 608,4 tokens ;
- moyenne B : 5 378,4 tokens ;
- moyenne C : 2 895,8 tokens ;
- réduction C face à B : 46,2 % ;
- réduction C face à A : 37,2 %.

Le taux de réussite d’un modèle et ses tokens de sortie restent `NOT_MEASURED`, car aucun runner de modèle contrôlé n’était disponible. Le rapport ne les invente pas.

## Commandes de diagnostic

```bash
arch-harness observed
arch-harness target
arch-harness context overview
arch-harness context build --focus <node> --radius 1 --max-items 50
arch-harness rules validate
arch-harness rules list
arch-harness stale
arch-harness doctor
arch-harness benchmark --mode v1.1
```

### Le graphe est stale

Exécuter `scripts/refresh_graph.sh`, puis `arch-harness stale`. Ne pas contourner le contrôle en modifiant manuellement le manifest.

### Une règle ne détecte rien

Vérifier que ses rôles correspondent à au moins un identifiant réel Graphify. Une règle dont la source ne résout aucun nœud peut passer sans évaluer d’entité ; `doctor` garantit que la référence est déclarée, mais les tests de production doivent aussi prouver sa résolution.

### Une violation semble fausse

Inspecter le matcher, le chemin minimal et la provenance. Les relations `AMBIGUOUS` ne provoquent pas de FAIL dur. Une allowlist ciblée est préférable à une règle trop large.

### Le contexte est trop volumineux

Réduire `--radius` ou `--max-items`, puis mesurer de nouveau. Ne pas supprimer une information nécessaire uniquement pour améliorer un pourcentage.

## Limites assumées

- Le parser Mermaid prend en charge un sous-ensemble ciblé : `flowchart`/`graph`, directions courantes, nœuds, labels, arêtes dirigées et subgraphs.
- Le parser YAML des règles est volontairement restreint au contrat V1.1.
- Le moteur analyse la topologie fournie par Graphify ; il ne prouve pas des propriétés métier ou de sécurité arbitraires.
- Les matchers sont lexicaux et explicites.
- APE est optionnel et n’était pas disponible pendant la validation.
- Le benchmark mesure le contexte, pas la qualité d’un modèle externe.

## Résultats et traçabilité

- Rapport final : `experiments/results/V1_1_FINAL_REPORT.md`
- Journal d’exécution : `logs/V1_1_IMPLEMENTATION_LOG.md`
- Métriques : `logs/V1_1_METRICS.md`
- Conversions ACE : `logs/V1_1_ACE_VALIDATION_LOG.md`
- Baseline V1 : tag Git `v1.0.0`

