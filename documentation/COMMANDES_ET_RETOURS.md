# Référence des commandes et retours d’Architecture Harness V2.2

## 1. Convention générale

La CLI est :

```bash
arch-harness [--root CHEMIN] COMMANDE
```

`--root` désigne la racine du projet consommateur. Sans option, le répertoire courant est utilisé.

Exemple :

```bash
arch-harness --root /projets/orders doctor
```

## 2. Codes de sortie

| Code | Signification | Action attendue |
|---:|---|---|
| 0 | `PASS`, `WARN` ou `NOT_APPLICABLE` | continuer, en conservant les advisories |
| 1 | violation bloquante `error + validated` | corriger le code, refresh, relancer le gate |
| 2 | erreur technique/configuration ou `UNRESOLVED` | exécuter `doctor`, réparer les mappings ou l’environnement |

Le code doit être lu avec le champ `status`. Le code 2 peut désigner une erreur technique ou une règle obligatoire impossible à évaluer.

En shell :

```bash
arch-harness gate --format json
result=$?
echo "$result"
```

## 3. Statuts d’évaluation

### `PASS`

Toutes les règles bloquantes applicables sont évaluées et respectées.

```json
{
  "status": "PASS",
  "blocking": false,
  "blocking_violations": []
}
```

### `WARN`

Une candidate, un warning ou une advisory est présente, mais rien ne bloque.

```json
{
  "status": "WARN",
  "blocking": false,
  "advisories": [
    {
      "rule_id": "candidate-rule",
      "severity": "warning"
    }
  ]
}
```

### `FAIL`

Au moins une règle `severity: error` et `status: validated` est violée.

```json
{
  "status": "FAIL",
  "blocking": true,
  "blocking_violations": [
    {
      "rule_id": "controller-must-not-call-repository",
      "source": "Controller",
      "target": "Repository"
    }
  ]
}
```

### `UNRESOLVED`

Une règle validée `applicability: required` ne trouve pas sa source ou sa cible Graphify. La règle n’a pas été vérifiée et ne doit pas être présentée comme `PASS`.

```json
{
  "status": "UNRESOLVED",
  "rule_assessments": [
    {
      "rule_id": "controller-must-use-service",
      "status": "UNRESOLVED",
      "source_matches": [],
      "target_matches": []
    }
  ]
}
```

### `NOT_APPLICABLE`

Une règle `when_observed` concerne un composant futur ou optionnel encore absent. Cette absence est normale et non bloquante.

### `ERROR`

La commande n’a pas pu exécuter le contrôle, par exemple à cause d’un graphe périmé :

```json
{
  "status": "ERROR",
  "error": "STALE_GRAPH",
  "files": ["src/orders.py"]
}
```

## 4. `doctor`

```bash
arch-harness doctor
arch-harness agent doctor --format json
```

Contrôle :

- validité de `graphify-out/graph.json` ;
- parsing Mermaid officiel ;
- syntaxe des règles et mappings ;
- fraîcheur Graphify ;
- écriture du cache.

Retour texte :

```text
PASS Graphify output: valid
PASS target Mermaid: valid
PASS context Mermaid: valid
PASS rules and mappings: valid
PASS Graphify freshness: manifest hashes match source files
PASS cache: writable
```

Utiliser `agent doctor` lorsqu’un orchestrateur préfère du JSON.

## 5. `graph refresh`

```bash
arch-harness graph refresh --format json
```

Lance Graphify sur le projet. Au premier passage, une extraction est créée ; ensuite une mise à jour incrémentale est utilisée.

Champs principaux :

```json
{
  "status": "PASS",
  "mode": "update",
  "fresh": true,
  "graph": "/projet/graphify-out/graph.json",
  "summary": {
    "nodes": 120,
    "edges": 245,
    "extracted": 230,
    "inferred": 15,
    "ambiguous": 0
  }
}
```

Cette commande modifie les sorties Graphify. Le gate, lui, reste en lecture seule.

## 6. `stale`

```bash
arch-harness stale
```

Vérifie seulement la fraîcheur du graphe.

Retour valide :

```text
fresh: true
```

Retour périmé :

```text
fresh: false
stale: src/orders.py
```

## 7. `observed`

```bash
arch-harness observed
```

Résume le graphe Graphify :

```text
nodes: 120
edges: 245
extracted: 230
inferred: 15
ambiguous: 0
```

Cette commande n’évalue aucune règle.

## 8. `target`

```bash
arch-harness target
```

Parse les Mermaid d’architecture et affiche leur normalisation :

```text
nodes: Controller, Repository, Service
edges:
  Controller -> Service
  Service -> Repository
subgraphs:
  Orders: Controller, Repository, Service
```

Une erreur indique que Mermaid officiel a rejeté le diagramme ou que le runtime Node est indisponible.

## 9. `rules validate`

```bash
arch-harness rules validate
arch-harness rules validate --file architecture/rules/candidates.yaml
```

Sans `--file`, valide `architecture/rules/rules.yaml`.

Retour :

```text
valid: 3 rules, 4 roles
```

La validation porte sur la structure, les types, les rôles, les statuts, la provenance et l’applicabilité. Elle ne promeut aucune candidate.

## 10. `rules list`

```bash
arch-harness rules list
```

Affiche les règles :

```text
controller-must-use-service: required_edge Controller -> Service
controller-must-not-call-repository: forbidden_edge Controller -> Repository
```

## 11. `rules author-context`

```bash
arch-harness rules author-context --format json
```

Produit l’entrée du skill `architecture-rule-author`.

Champs principaux :

- `diagram_types` : types reconnus par Mermaid officiel ;
- `diagrams` : chemin et texte complet des Mermaid ;
- `declared_facts.nodes` : composants déclarés ;
- `declared_facts.edges` : directions déclarées ;
- `declared_facts.subgraphs` : regroupements ;
- `mapping_proposals` : correspondances Graphify classées ;
- `instructions` : traitement de chaque état.

Exemple réduit :

```json
{
  "status": "PASS",
  "diagram_types": ["architecture"],
  "mapping_proposals": [
    {
      "declared_id": "Controller",
      "declared_label": "Order Controller",
      "status": "resolved_candidate",
      "candidates": [
        {
          "graphify_id": "src_orders_controller_ordercontroller",
          "file": "src/orders/controller.py",
          "kind": "code",
          "score": 1.45
        }
      ]
    }
  ]
}
```

La commande ne choisit pas une politique et n’écrit pas les règles. Le skill LLM exploite ces preuves pour écrire des candidates.

## 12. `context overview`

```bash
arch-harness context overview
```

Résume les Mermaid de `contexte/` :

```text
nodes: 12
edges: 18
provenance: DECLARED_CONTEXT
```

## 13. `context build`

```bash
arch-harness context build --focus OrderController
```

Options :

```text
--focus       répétable, au moins une fois
--radius      rayon du voisinage, défaut 1
--max-items   limite de résultats, défaut 50
```

Retour texte destiné au diagnostic humain : code observé, contexte déclaré, architecture cible, règles applicables, fichiers pertinents et indication de troncature.

Si aucun nœud ne correspond :

```text
configuration error: No focus node matches the observed or declared graphs
```

## 14. `agent context`

```bash
arch-harness agent context \
  --focus OrderController \
  --radius 1 \
  --max-items 50 \
  --format json
```

Version JSON stable de `context build`, conçue pour les orchestrateurs.

Champs :

- `observed_code` ;
- `declared_context` ;
- `target_architecture` ;
- `applicable_rules` ;
- `relevant_files` ;
- `provenance` ;
- `metrics.context_tokens` ;
- `metrics.truncated`.

Si `truncated` vaut `true`, l’agent peut relancer avec un focus plus précis ou une limite plus élevée.

## 15. `check`

```bash
arch-harness check
arch-harness check --format json
arch-harness check --format markdown
```

Évalue les règles avec trois formats possibles :

- `text` : lecture terminal ;
- `json` : automatisation ;
- `markdown` : rapport humain.

Contrairement au gate, `check` ne réalise pas lui-même le contrôle préalable de fraîcheur. Pour un checkpoint CI ou agentique, préférer `gate`.

## 16. `gate`

```bash
arch-harness gate --format json
```

Checkpoint recommandé. Il :

1. vérifie la fraîcheur Graphify ;
2. charge le graphe observé ;
3. parse les Mermaid ;
4. charge les règles validées ;
5. évalue les règles ;
6. sépare violations bloquantes et advisories ;
7. retourne le code approprié.

Champs essentiels :

```text
status
blocking
blocking_violations
advisories
rule_assessments
```

Chaque assessment contient :

```text
rule_id
status
reason
source_matches
target_matches
```

## 17. `agent validate`

```bash
arch-harness agent validate --format json
```

Évaluation JSON destinée à un agent. Elle refuse également un graphe périmé et retourne les mêmes codes que le moteur.

## 18. `capabilities`

```bash
arch-harness capabilities --format json
arch-harness agent capabilities --format json
```

Permet à un orchestrateur de découvrir :

- les commandes publiques ;
- les formats ;
- les types de règles ;
- les applicabilités ;
- les statuts ;
- les provenances ;
- les codes de sortie ;
- les skills disponibles.

Extrait :

```json
{
  "api_version": "2.0",
  "commands": {
    "rule_author_context": "arch-harness rules author-context --format json",
    "gate": "arch-harness gate --format json"
  },
  "orchestrator_skills": ["architecture-rule-author"],
  "llm_in_policy_engine": false
}
```

## 19. `integrations install`

### BMAD

```bash
arch-harness integrations install bmad \
  --adapter-root /chemin/architecture-harness
```

Prérequis : BMAD doit déjà être installé avec un répertoire `_bmad/`.

Installe les trois overrides et `.agents/skills/architecture-rule-author/`.

### Codex

```bash
arch-harness integrations install codex \
  --adapter-root /chemin/architecture-harness
```

Installe le Rule Author et ajoute un bloc géré dans `AGENTS.md`.

### Claude Code

```bash
arch-harness integrations install claude \
  --adapter-root /chemin/architecture-harness
```

Installe les deux skills Claude et ajoute un bloc géré dans `CLAUDE.md`.

### Protection contre l’écrasement

L’installateur refuse d’écraser un skill ou override existant :

```text
configuration error: Refusing to overwrite existing orchestrator asset ...
```

Après comparaison manuelle, `--force` autorise le remplacement des assets gérés :

```bash
arch-harness integrations install codex \
  --adapter-root /chemin/architecture-harness \
  --force
```

## 20. `benchmark`

```bash
arch-harness benchmark --mode v1
arch-harness benchmark --mode v1.1
arch-harness benchmark --mode v2
arch-harness benchmark --mode v2 --tasks experiments/tasks.yaml
```

Compare différentes conditions de contexte et mesure les tokens. Il ne mesure pas automatiquement la réussite métier d’un LLM.

## 21. Commandes ACE expérimentales

Compiler une contrainte contrôlée :

```bash
arch-harness ace compile \
  --text "Controller MUST NOT directly depend on Repository"
```

Valider un fichier avec l’adaptateur APE lorsqu’il est disponible :

```bash
arch-harness ace validate chemin/regle.txt
```

Ces commandes sont expérimentales et ne remplacent pas le lifecycle de validation humaine.

## 22. Erreurs de configuration courantes

### Node.js absent

```text
configuration error: Node.js is required by the official Mermaid parser runtime
```

Installer Node.js 20+ et lancer `npm ci` dans le dépôt Harness.

### Mermaid invalide

```text
configuration error: target.mmd: Mermaid parser rejected diagram: ...
```

Corriger le fichier avec Mermaid officiel ou Mermaid Live.

### Graphify absent

Installer les dépendances Python du Harness puis vérifier :

```bash
graphify --help
arch-harness graph refresh --format json
```

### Graphe périmé

```json
{
  "status": "ERROR",
  "error": "STALE_GRAPH"
}
```

Exécuter `graph refresh`, puis relancer le gate.

### Mapping non résolu

Exécuter :

```bash
arch-harness rules author-context --format json
```

Faire traiter la sortie par `architecture-rule-author`. Corriger le mapping candidat ou confirmer l’ambiguïté ; ne pas supprimer la règle pour obtenir `PASS`.

## 23. Séquence recommandée pour une story

```bash
# Avant le code
arch-harness agent context --focus <composant> --format json

# Après une étape cohérente
pytest -q                         # ou tests du langage
arch-harness graph refresh --format json
arch-harness gate --format json

# Si Mermaid ou mappings ont changé
arch-harness rules author-context --format json

# Avant livraison
arch-harness doctor
arch-harness graph refresh --format json
arch-harness gate --format json
```

Le résultat attendu pour livrer est : tests fonctionnels passants, gate sans violation bloquante, mappings obligatoires résolus et revue de code terminée.
