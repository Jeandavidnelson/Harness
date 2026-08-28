# V2 Implementation Log

Date/time values use Europe/Paris. Unavailable metrics are `NOT_MEASURED`. Negative results are retained.

## Gate 0 — V2 Challenge — 2026-08-28

### Objective
Attempt to falsify the proposed V2 before implementing it.

### Hypothesis
The V1.1 core provides enough differentiated value and evidence to justify a BMAD-first V2.

### Implementation
Inspected V1.1 code-facing context, rules, tests, logs, metrics, reports, integration documents, Git state and the complete V2 plan. Produced `experiments/V2_CHALLENGE_REPORT.md`.

### Commands
- `git status --short --branch`
- `arch-harness stale`
- `arch-harness agent context --focus architecture_harness --format json`
- repository inventory and document inspection

### Tests
No new functionality was introduced. Freshness check: PASS.

### Metrics
- existing normalized architecture context: 3547 tokens
- applicable existing rules: 8
- existing observed context edges returned: 50 (truncated)
- V1.1 model task success: NOT_MEASURED
- V1.1 real BMAD runs: 0
- V1.1 real autonomous correction runs: 0

### Negative findings
- unresolved rule sources can pass vacuously;
- rule evaluation ignores relation type;
- target Mermaid is guidance, not a meaningful blocking comparator by itself;
- correction tests mutate graphs in memory rather than using real agents;
- BMAD integration is untested documentation;
- rule-maintenance cost and clarification count are unmeasured.

### Correction to plan
Proceed only with explicit rule lifecycle, blocking semantics, mapping diagnostics, Test Lab evidence and adapter-only BMAD integration. Do not auto-promote Mermaid or LLM inference.

### Result
`PROCEED WITH CHANGES`.

### Commit
Pending Gate 0 commit.

### Status
PASS — challenge completed; Gate 1 may begin only after commit.

## Gate 1 — V1.1 Regression Baseline — 2026-08-28

### Objective
Reproduce all V1.1 gates before introducing V2 behavior.

### Hypothesis
The tagged/documented V1.1 implementation remains operational on the current repository and environment.

### Implementation
Executed pytest, doctor, harness JSON check, real A/B/C benchmark and the complete V1.1 validation script. Recorded `experiments/results/V2_BASELINE.md`.

### Commands
- `.venv/bin/pytest -q`
- `.venv/bin/arch-harness doctor`
- `.venv/bin/arch-harness check --format json`
- `.venv/bin/arch-harness benchmark --mode v1.1`
- `scripts/validate_v1_1.sh`

### Tests
- full suite: 40 passed;
- ACE focused suite: 3 passed;
- skill validator: PASS;
- doctor: PASS;
- harness: PASS.

### Metrics
- Graphify: 0.9.50;
- raw/normalized nodes: 555 / 569;
- edges: 1033;
- C versus B context reduction: 46.2%;
- observed aggregate wall time: 13 seconds;
- model task success: NOT_MEASURED.

### Negative findings
The successful regression run still has no real BMAD execution, no real autonomous implementation, no lifecycle/severity semantics and no maintenance-cost measurement.

### Result
V1.1 baseline is reproducible without failures.

### Commit
Pending Gate 1 commit.

### Status
PASS — Gate 2 may begin after commit.

## Gate 2 — Production Graphify Integration — 2026-08-28

### Objective
Expose the proven production Graphify refresh through the universal core CLI.

### Hypothesis
Adapters can refresh observed architecture without knowing Graphify command details or shell-script paths.

### Implementation
Added `architecture_harness.graphify_runtime`, `arch-harness graph refresh --format json`, extract/update selection, executable discovery, post-refresh freshness verification and normalized summary. Reduced `scripts/refresh_graph.sh` to a compatibility wrapper around the core CLI.

### Commands
- `arch-harness graph refresh --format json`
- pytest
- `arch-harness agent validate --format json`

### Tests
- full suite: 43 passed;
- real `graph refresh`: PASS;
- freshness verification: PASS;
- agent validation: PASS;
- diff whitespace check: PASS.

### Metrics
- normalized nodes: 614;
- edges: 1104;
- EXTRACTED / INFERRED / AMBIGUOUS: 1031 / 73 / 0;
- refresh duration reported by the CLI: 0.8931 seconds.

### Problems / negative results
Graphify still uses its own confidence vocabulary (`EXTRACTED`, `INFERRED`, `AMBIGUOUS`). V2 origin provenance remains a distinct concern for Gate 3.

### Commit
Pending Gate 2 commit.

### Status
PASS — the shell wrapper and adapters can rely on the universal CLI contract.

## Gate 3 — Provenance Model — 2026-08-28

### Objective
Separate the origin of architectural evidence from extractor confidence.

### Hypothesis
Agents can reason safely when declared, observed, inferred, confirmed, generated and ambiguous facts are explicit without discarding Graphify's native confidence.

### Implementation
Added the six-value `EvidenceOrigin` model, deterministic confidence-to-origin mapping, explicit Mermaid declaration origin, and origin fields in agent context/capabilities. Kept the existing `provenance` field as extractor confidence for backward compatibility.

### Commands
- `arch-harness agent context --focus ir --format json`
- `scripts/refresh_graph.sh`
- `pytest -q`
- `arch-harness agent validate --format json`

### Tests
- first run: 43 passed, 2 failed because the stale-graph guard correctly rejected changed source files;
- after required Graphify refresh: 45 passed;
- agent validation: PASS;
- diff whitespace check: PASS.

### Metrics
- supported evidence origins: 6;
- new provenance tests: 2;
- hidden provenance promotions: 0.

### Problems / negative results
The legacy field name `provenance` represents Graphify confidence, not evidence origin. It remains temporarily supported to avoid a breaking V1.1 migration; V2 payloads expose both dimensions.

### Status
PASS — provenance is explicit and deterministic; inferred facts are not promoted.

## Gate 4 — Universal Agent API — 2026-08-28

### Objective
Provide a discoverable, orchestrator-neutral CLI contract.

### Hypothesis
A generic consumer can discover and call the harness without importing Python internals or knowing BMAD.

### Implementation
Promoted capabilities to the top-level CLI, versioned the contract as `2.0`, advertised canonical commands and exit codes, and declared the absence of an orchestrator dependency. Preserved the V1.1 `agent capabilities` alias.

### Functional and behavior tests
- full suite: 47 passed;
- an external subprocess discovered capabilities and requested a bounded context;
- direct capabilities and five-item context smoke tests: PASS;
- graph freshness and diff whitespace: PASS.

### Metrics
- stable advertised commands: 6;
- context returned to generic test: at most 5 observed edges;
- core orchestrator dependencies: 0.

### Problems / negative results
The advertised `gate` endpoint is intentionally not callable until Gate 5. Capability discovery leads implementation by one committed gate, but no adapter is shipped against it yet.

### Status
PASS — BMAD, Codex and other consumers can share one machine-readable contract.

## Gate 5 — Architecture Gate Lifecycle — 2026-08-28

### Objective
Expose an immutable, deterministic checkpoint with stable exit semantics.

### Hypothesis
Any orchestrator can decide when to invoke the architecture gate while the core remains read-only and orchestration-neutral.

### Implementation
Added `arch-harness gate --format json`, stale-graph refusal, `PASS`/`FAIL`/technical `ERROR` semantics, blocking/advisory collections and a pure gate payload builder. The command evaluates existing inputs but never refreshes or edits code.

### Functional and behavior tests
- full suite: 49 passed;
- current repository gate: PASS, exit 0;
- agent validation parity: PASS;
- gate payload failure behavior: PASS;
- source hash before/after gate unchanged: PASS.

### Metrics
- gate code mutations: 0;
- blocking violations in current repository: 0;
- exit classes: 3.

### Problems / negative results
Until Gate 6 adds severity and validation status, every V1 rule remains blocking for backward compatibility and advisories remain empty.

### Status
PASS — checkpoint control belongs to the consuming workflow, not the core.

## Gate 6 — Candidate / Validated Rule Lifecycle — 2026-08-28

### Objective
Prevent generated or unreviewed architecture interpretations from becoming hard policy.

### Hypothesis
Rule findings can remain useful to agents without blocking until a human explicitly validates an error-level rule.

### Implementation
Extended Rule IR with allowed targets, severity, scope, exceptions, rationale, provenance and lifecycle status. Added the complete proposed-to-validated vocabulary, candidate and decision files, enriched violation evidence, and PASS/WARN/FAIL partitioning. Existing production rules are explicitly `error`, `USER_CONFIRMED`, `validated`; candidate rules remain outside the blocking rules file.

### Functional and behavior tests
- full suite: 51 passed;
- current architecture gate: PASS;
- production rule validation: 8 rules / 9 roles;
- candidate error violation: WARN/non-blocking;
- validated warning violation: WARN/non-blocking;
- validated error violation: FAIL/blocking.

### Metrics
- validated production rules: 8;
- unpromoted example candidates: 1;
- lifecycle states supported: 5;
- severities supported: 3;
- automatic candidate promotions: 0.

### Problems / negative results
Scope and exceptions are preserved in the IR but do not yet alter matching; using them as active policy without defined semantics would be unsafe. Candidate promotion remains a deliberate file review, not an automatic CLI mutation.

### Status
PASS — only human-confirmed validated errors can hard-fail the gate.

## Gate 7 — Architecture Rule Authoring Skill — 2026-08-28

### Objective
Package the Mermaid-to-candidate workflow as a reusable agent skill.

### Hypothesis
An agent can derive reviewable candidates while preserving human control over blocking policy.

### Implementation
Used the official skill-creator workflow to initialize `skills/architecture-rule-author`, added concise authoring and clarification instructions, safety boundaries, candidate schema, UI metadata and a CLI `--file` option for candidate validation.

### Functional and behavior tests
- official `quick_validate.py`: PASS under the project virtual environment;
- candidate file validation: 1 rule / 2 roles;
- full suite: 52 passed;
- architecture gate: PASS;
- static safety-boundary behavior assertions: PASS.

### Metrics
- candidate rules created by the skill implementation: 1 example;
- rules promoted: 0;
- clarification questions in this implementation run: 0 (requirements were explicit);
- real forward-test agent runs: 0.

### Problems / negative results
The system Python lacked PyYAML, so the official validator was rerun successfully with `.venv/bin/python`. No subagent forward-test was run because current execution instructions prohibit spawning subagents unless explicitly requested; Gate 9 remains responsible for real-agent evidence through available external runners.

### Status
PASS for packaging and deterministic behavior; real-agent generalization remains NOT_MEASURED.
