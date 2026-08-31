# Installation avec Claude Code, BMAD, Codex ou GitHub Copilot

Ce guide part d’une machine neuve et distingue deux emplacements :

- `/opt/architecture-harness` : clone du produit Architecture Harness ;
- `/projets/mon-app` : projet que vous voulez protéger.

Remplacez ces chemins par les vôtres. Les commandes macOS/Linux utilisent un environnement virtuel Python local.

## Légende des responsabilités

| Icône | Responsable | Signification dans ce guide |
|---|---|---|
| 👤 | Utilisateur | commande d’installation, choix ou validation à effectuer soi-même |
| 🤖 | Agent / orchestrateur | action attendue de Codex, Claude, BMAD ou Copilot |
| ⚙️ | Automatique | opération exécutée par le Harness, Graphify ou le gate |

## 1. Prérequis

- Git ;
- Python 3.10 ou plus récent ;
- Node.js 20 ou plus récent et npm ;
- l’orchestrateur choisi ;
- `uv` en plus pour BMAD 6.11.

Vérification :

```bash
git --version
python3 --version
node --version
npm --version
```

## 2. 👤 Installer Architecture Harness

```bash
git clone <URL_DU_DEPOT> /opt/architecture-harness
cd /opt/architecture-harness
python3 -m venv .venv
.venv/bin/python -m pip install --upgrade pip
.venv/bin/python -m pip install -e '.[dev]'
npm ci
.venv/bin/arch-harness doctor
```

Pourquoi ces commandes :

| Commande | Utilité |
|---|---|
| `python3 -m venv .venv` | isole Python et la CLI du système |
| `pip install -e '.[dev]'` | installe `arch-harness`, Graphify et les outils de validation |
| `npm ci` | installe le parseur Mermaid officiel dans ses versions verrouillées |
| `arch-harness doctor` | vérifie l’installation et les fichiers attendus |

Pour valider le dépôt du Harness lui-même :

```bash
cd /opt/architecture-harness
scripts/validate_v2.sh
```

## 3. 👤 Préparer le projet cible

```bash
cd /projets/mon-app
python3 -m venv .venv
.venv/bin/python -m pip install -e '/opt/architecture-harness[dev]'
export PATH="$PWD/.venv/bin:$PATH"
mkdir -p architecture/diagrams architecture/rules contexte
```

Créez `architecture/diagrams/target.mmd` :

```mermaid
architecture-beta
group app(cloud)[Application]
service controller(server)[Controller] in app
service app_service(server)[Service] in app
service repository(database)[Repository] in app
controller:R --> L:app_service
app_service:R --> L:repository
```

Créez `architecture/rules/rules.yaml` et `architecture/rules/candidates.yaml` :

```yaml
roles: {}
rules: []
```

Créez `architecture/rules/decisions.md` :

```markdown
# Décisions d’architecture

Aucune règle promue pour le moment.
```

Créez `contexte/runtime.mmd` :

```mermaid
sequenceDiagram
    participant Client
    participant Controller
    participant Service
    Client->>Controller: request
    Controller->>Service: execute
```

Vérifiez la base :

```bash
arch-harness --root "$PWD" target
arch-harness --root "$PWD" rules validate
arch-harness --root "$PWD" rules author-context --format json
```

Dans un projet greenfield sans code, l’état `pending_code` est normal.

## 3.1 Comprendre le résultat d’un installateur

Les installateurs Codex, Claude et BMAD retournent un JSON. L’installation n’est confirmée que si :

- `status` vaut `PASS` ;
- `integration` correspond à l’orchestrateur demandé ;
- chaque chemin de `installed` existe dans le projet cible ;
- `core_dependency_added` vaut `false`, car l’adaptateur reste découplé du core.

Exemple réel pour Codex :

```json
{
  "core_dependency_added": false,
  "installed": [
    ".agents/skills/architecture-rule-author/SKILL.md",
    ".agents/skills/architecture-rule-author/agents/openai.yaml",
    "AGENTS.md"
  ],
  "integration": "codex",
  "status": "PASS"
}
```

La vérification se fait en deux niveaux :

1. 👤 **installation** : le JSON vaut `PASS` et les fichiers annoncés existent ;
2. ⚙️ **fonctionnement de bout en bout** : après la présence de code, `graph refresh`, `doctor` et `gate` réussissent.

Ne lancez pas `doctor` comme seule preuve dans un projet greenfield vide : l’absence normale du premier graphe serait signalée. Commencez par vérifier `target`, `rules validate` et `rules author-context`.

## 4. Installer avec Codex

### 👤 Étape 1 — installer l’adaptateur

Depuis le projet cible :

```bash
arch-harness --root "$PWD" integrations install codex \
  --adapter-root /opt/architecture-harness
```

Cette commande :

- copie le skill dans `.agents/skills/architecture-rule-author/` ;
- ajoute un bloc géré à `AGENTS.md` ;
- conserve le cœur indépendant de Codex.

### 👤 Étape 2 — vérifier les fichiers

```bash
test -f AGENTS.md
test -f .agents/skills/architecture-rule-author/SKILL.md
test -f .agents/skills/architecture-rule-author/agents/openai.yaml
rg -n "Architecture Harness" AGENTS.md
rg -n '^name: architecture-rule-author$' \
  .agents/skills/architecture-rule-author/SKILL.md
```

Chaque commande doit sortir avec le code `0`. Vérifiez aussi que le JSON d’installation contient exactement `integration: "codex"` et `status: "PASS"`.

### 🤖 Étape 3 — tester dans Codex

Demande d’essai :

```text
Lis le contexte Architecture Harness pour OrderService, ajoute une petite évolution,
exécute les tests, rafraîchis le graphe et valide l’architecture.
```

Codex doit exécuter :

```bash
# 🤖 contexte demandé par Codex
arch-harness agent context --focus OrderService --format json
# 🤖 modification et tests
# ⚙️ opérations exécutées par les outils
arch-harness graph refresh --format json
arch-harness agent validate --format json
```

Après un changement Mermaid, il doit utiliser automatiquement `$architecture-rule-author`.

### ⚙️ Étape 4 — preuve de fonctionnement

Après qu’un premier fichier source existe :

```bash
arch-harness graph refresh --format json
arch-harness agent doctor --format json
arch-harness agent context --focus <NOEUD_REEL> --format json
arch-harness agent validate --format json
```

Installation correcte : `graph refresh` et `doctor` retournent `status: "PASS"`, le contexte contient le nœud demandé et `agent validate` ne retourne aucune erreur technique.

## 5. Installer avec Claude Code

### 👤 Étape 1 — installer l’adaptateur

```bash
arch-harness --root "$PWD" integrations install claude \
  --adapter-root /opt/architecture-harness
```

Cette commande installe :

```text
.claude/skills/architecture-harness/
.claude/skills/architecture-rule-author/
CLAUDE.md
```

### 👤 Étape 2 — vérifier les fichiers

```bash
test -f CLAUDE.md
test -f .claude/skills/architecture-harness/SKILL.md
test -f .claude/skills/architecture-rule-author/SKILL.md
test -f .claude/skills/architecture-rule-author/agents/openai.yaml
rg -n "Architecture Harness" CLAUDE.md
rg -n '^name: architecture-harness$' \
  .claude/skills/architecture-harness/SKILL.md
rg -n '^name: architecture-rule-author$' \
  .claude/skills/architecture-rule-author/SKILL.md
```

Chaque commande doit sortir avec le code `0`. Le JSON d’installation doit contenir `integration: "claude"`, `status: "PASS"` et les quatre fichiers ci-dessus.

### 🤖 Étape 3 — tester dans Claude Code

Demande d’essai :

```text
Implémente cette évolution en respectant Architecture Harness. Utilise le contexte
compact avant le code et le gate après les tests.
```

Le skill `/architecture-harness` impose le cycle contexte → code/tests → refresh → gate. Après un changement Mermaid ou un mapping non résolu, `/architecture-rule-author` prépare les candidates. La promotion reste soumise à votre approbation explicite.

### ⚙️ Étape 4 — preuve de fonctionnement

Après la création du premier code, demandez à Claude d’exécuter le cycle, puis contrôlez manuellement :

```bash
arch-harness graph refresh --format json
arch-harness agent doctor --format json
arch-harness gate --format json
```

Les sorties attendues sont `PASS`. Si Claude ne lance pas les commandes, vérifiez qu’il a bien chargé `CLAUDE.md` et les deux fichiers `SKILL.md`.

## 6. Installer avec BMAD

Le terme « BMAD » désigne ici BMAD Method 6.11 ou plus récent.

### 👤 Étape 1 — installer BMAD et `uv`

```bash
cd /projets/mon-app
npx bmad-method install --modules bmm --tools codex
python3 -m pip install uv
```

`uv` est requis par les workflows Build de BMAD 6.11.

### 👤 Étape 2 — installer l’adaptateur Harness

```bash
arch-harness --root "$PWD" integrations install bmad \
  --adapter-root /opt/architecture-harness
```

L’installateur vérifie que `_bmad/` existe, puis copie :

```text
_bmad/custom/bmad-architecture.toml
_bmad/custom/bmad-build.toml
_bmad/custom/bmad-code-review.toml
.agents/skills/architecture-rule-author/
```

### 👤 Étape 3 — vérifier

```bash
test -f _bmad/custom/bmad-architecture.toml
test -f _bmad/custom/bmad-build.toml
test -f _bmad/custom/bmad-code-review.toml
test -f .agents/skills/architecture-rule-author/SKILL.md
test -f .agents/skills/architecture-rule-author/agents/openai.yaml
rg -n "arch-harness" _bmad/custom/*.toml
rg -n '^name: architecture-rule-author$' \
  .agents/skills/architecture-rule-author/SKILL.md
```

Chaque commande doit sortir avec le code `0`. Le JSON d’installation doit annoncer `integration: "bmad"`, `status: "PASS"` et cinq fichiers installés.

### 👤/🤖 Étape 4 — utiliser le workflow

```mermaid
flowchart TD
    A["👤 $bmad-architecture"] --> M["👤 Mermaid"]
    M --> R["🤖 $architecture-rule-author"]
    R --> H["👤 Revue et validation humaine"]
    H --> B["🤖 $bmad-build"]
    B --> C["🤖 Contexte compact + code + tests"]
    C --> G["⚙️ Graph refresh + gate"]
    G -->|"FAIL"| B
    G -->|"PASS"| V["$bmad-code-review"]
```

Ordre recommandé :

1. 👤 lancez `$bmad-architecture` pour concevoir ou mettre à jour Mermaid ;
2. 🤖 laissez `$architecture-rule-author` créer les candidates ;
3. 👤 révisez et approuvez explicitement les règles souhaitées ;
4. 👤 lancez `$bmad-build` pour implémenter ;
5. ⚙️ laissez le workflow boucler sur Graphify et le gate ;
6. 🤖 terminez par `$bmad-code-review`.

Après le premier code greenfield, BMAD relance `graph refresh` puis `rules author-context` pour résoudre les mappings qui étaient `pending_code`.

### ⚙️ Étape 5 — preuve de fonctionnement

Après un premier `$bmad-build`, vérifiez hors du chat :

```bash
arch-harness graph refresh --format json
arch-harness agent doctor --format json
arch-harness gate --format json
```

Puis lancez `$bmad-code-review` et vérifiez qu’il charge le verdict architectural. Un gate PASS prouve l’intégration architecturale, mais pas le comportement métier.

## 7. Installer avec GitHub Copilot

Architecture Harness V2.2 n’expose pas encore de commande `integrations install copilot`. Copilot utilise donc l’intégration générique : une instruction de dépôt appelle la même CLI stable. Cette méthode ne nécessite aucun SDK.

### 👤 Étape 1 — créer les instructions Copilot

Créez `.github/copilot-instructions.md` avec ce contenu :

```markdown
# Architecture Harness

Avant toute modification significative, exécuter :

`arch-harness agent context --focus <noeud-pertinent> --format json`

Après les tests et à chaque checkpoint cohérent, exécuter :

`arch-harness graph refresh --format json`

`arch-harness gate --format json`

Un code 1 impose de corriger toutes les violations bloquantes puis de répéter refresh
et gate. Un code 2 impose `arch-harness agent doctor --format json`. Ne jamais modifier
une règle validée uniquement pour obtenir PASS.

Après une modification Mermaid, un premier graphe greenfield ou un mapping non résolu,
lire `skills/architecture-rule-author/SKILL.md`, exécuter
`arch-harness rules author-context --format json`, puis écrire uniquement des candidates
non bloquantes sans promotion non approuvée.
```

### 👤 Étape 2 — rendre le skill accessible

Copiez le skill versionné dans le projet :

```bash
mkdir -p skills/architecture-rule-author
cp /opt/architecture-harness/skills/architecture-rule-author/SKILL.md \
  skills/architecture-rule-author/SKILL.md
```

### 🤖 Étape 3 — tester dans Copilot Chat

Demande d’essai :

```text
Avant de modifier OrderService, lis .github/copilot-instructions.md et récupère le
contexte compact Architecture Harness. Après les tests, rafraîchis le graphe et lance le gate.
```

Vérifiez dans le terminal que Copilot a bien exécuté :

```bash
arch-harness agent context --focus OrderService --format json
arch-harness graph refresh --format json
arch-harness gate --format json
```

Si votre édition de Copilot n’autorise pas l’exécution de commandes, lancez ces commandes vous-même et fournissez la sortie JSON au chat.

### 👤 Étape 4 — vérifier l’installation manuelle

```bash
test -f .github/copilot-instructions.md
test -f skills/architecture-rule-author/SKILL.md
rg -n "arch-harness agent context" .github/copilot-instructions.md
rg -n "arch-harness gate" .github/copilot-instructions.md
rg -n '^name: architecture-rule-author$' \
  skills/architecture-rule-author/SKILL.md
```

Ces cinq commandes doivent sortir avec le code `0`. Après la présence du premier code, exécutez aussi `graph refresh`, `agent doctor` et `gate` comme pour les autres orchestrateurs.

## 7.1 Tableau de diagnostic des intégrations

| Symptôme | Cause probable | Vérification | Correction |
|---|---|---|---|
| aucun skill détecté par Codex | skill absent ou mauvais projet racine | `test -f .agents/skills/architecture-rule-author/SKILL.md` | relancer l’installation avec le bon `--root` |
| Claude ignore le workflow | `CLAUDE.md` ou skill Harness absent | `test -f CLAUDE.md && test -f .claude/skills/architecture-harness/SKILL.md` | réinstaller l’adaptateur Claude |
| BMAD refuse l’installation | `_bmad/` n’existe pas | `test -d _bmad` | installer BMAD avant l’adaptateur |
| installateur refuse l’écrasement | asset déjà présent | lire le chemin dans l’erreur | comparer, sauvegarder, puis seulement utiliser `--force` |
| installation PASS mais gate en erreur | projet non initialisé ou graphe périmé | `arch-harness agent doctor --format json` | créer le code initial ou exécuter `graph refresh` |
| Copilot ne lance aucune commande | terminal non autorisé | vérifier les capacités de l’édition | exécuter la CLI manuellement et fournir le JSON |

## 8. 👤/🤖 Premier cycle commun

Quel que soit l’orchestrateur :

```bash
# 👤 1. vérifier la configuration
arch-harness doctor

# 🤖 2. obtenir le contexte avant le code
arch-harness agent context --focus OrderService --format json

# ⚙️ 3. après le code et les tests
arch-harness graph refresh --format json

# ⚙️ 4. contrôler l’architecture
arch-harness gate --format json
echo $?
```

Interprétation :

| Code | Résultat | Action |
|---:|---|---|
| 0 | PASS, WARN ou NOT_APPLICABLE | examiner les advisories puis continuer |
| 1 | violation architecturale bloquante | corriger le code et répéter les étapes 3–4 |
| 2 | problème technique/configuration | exécuter `arch-harness agent doctor --format json` |

## 9. 👤 Mettre à jour une intégration

Les installateurs refusent d’écraser un asset existant. Procédure sûre :

1. mettez à jour `/opt/architecture-harness` ;
2. comparez vos fichiers installés aux nouvelles versions ;
3. sauvegardez ou committez vos personnalisations ;
4. utilisez `--force` seulement après revue.

Exemple :

```bash
git -C /opt/architecture-harness pull
arch-harness --root /projets/mon-app integrations install codex \
  --adapter-root /opt/architecture-harness --force
```

## 10. 👤 Résolution des problèmes

### `arch-harness: command not found`

```bash
export PATH="/projets/mon-app/.venv/bin:$PATH"
# ou utilisez explicitement
/projets/mon-app/.venv/bin/arch-harness doctor
```

### `Graphify executable not found`

Installez les dépendances de développement dans l’environnement virtuel du projet :

```bash
.venv/bin/python -m pip install -e '/opt/architecture-harness[dev]'
```

### Mermaid ou runtime Node indisponible

```bash
cd /opt/architecture-harness
npm ci
node --version
```

### `STALE_GRAPH`

```bash
arch-harness graph refresh --format json
arch-harness gate --format json
```

### Mapping ambigu ou obligatoire absent

```bash
arch-harness rules author-context --format json
```

Examinez `mapping_proposals`. Le skill peut accepter un candidat clairement étayé ; demandez une décision humaine si plusieurs significations restent plausibles.

### L’installateur refuse un écrasement

Comparez les fichiers et conservez vos personnalisations. N’utilisez `--force` qu’après cette revue.

## 11. 👤 Test de recette minimal

Une installation est opérationnelle si les commandes suivantes réussissent :

```bash
arch-harness doctor
arch-harness target
arch-harness rules validate
arch-harness graph refresh --format json
arch-harness agent context --focus <NOEUD_REEL> --format json
arch-harness gate --format json
```

Le focus doit correspondre à un nœud déclaré ou observé. Sur un projet sans code, créez d’abord un fichier source significatif, puis relancez `graph refresh`.
