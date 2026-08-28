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

## Gate 8 — V2 Test Lab A–L — 2026-08-28

### Objective
Exercise the architecture semantics across twelve reproducible project situations and retain raw experiment records beyond pytest output.

### Hypothesis
Validated rules detect known direct and indirect violations without blocking legitimate unspecified dependencies or candidate interpretations.

### Implementation
Added an executable Test Lab covering A–L. Every record captures prompt, context, actions, modified files, before/after graph, verdict, correction, metrics, assessment and execution kind. Generated `experiments/agent-runs/V2_TEST_LAB_RESULTS.json`.

### Functional and behavior tests
- first behavior run: scenario B correction remained FAIL because its test policy incorrectly used `forbidden_path`;
- correction: split direct-edge and indirect-path policies;
- retest: 54 passed;
- 12/12 scenarios reproduced;
- current repository gate: PASS.

### Metrics
- known violation scenarios: 4;
- detected: 4;
- deterministic detection rate: 100%;
- deterministic false blocking rate: 0%;
- correction iterations in adversarial B: 1;
- real agent runs: 0.

### Problems / negative results
These are deterministic simulations, not evidence of model task success. The initial faulty B policy demonstrates why rule semantics must be tested rather than inferred from names.

### Status
PASS for deterministic Test Lab; agentic claims remain reserved for Gate 9.

## Gate 9 — Real Agent Correction Loops — 2026-08-28

### Objective
Observe whether an external coding agent can use compact context and gate feedback to correct a real code graph.

### Implementation and behavior
Created an isolated Python project, extracted it with production Graphify, confirmed an initial gate FAIL, and ran two independent ephemeral Codex CLI processes. Preserved prompts, actions, changes, verdicts and token usage in `experiments/agent-runs/V2_REAL_CODEX_CORRECTION.md`.

### Results
- real agent processes: 2;
- first process: gate PASS but runtime FAIL due to missing service module;
- second process: runtime PASS, then exposed an incorrectly modeled transitive rule;
- final independently verified runtime: PASS;
- final gate after correcting experimental rule semantics: PASS;
- agent edits to rules or diagrams: 0.

### Metrics
- correction iterations: 2;
- first-pass full task success: 0%;
- final runtime-and-gate success: 100% for this single task;
- rule-model defects discovered: 1;
- total reported input tokens: 433672 (380416 cached);
- total reported output tokens: 4563.

### Problems / negative results
The architecture gate accepted broken runtime code in the first pass. A badly chosen `forbidden_path` also encouraged architecture-check gaming. These results reinforce that the harness complements tests and review and that rule authoring quality is critical.

### Status
PASS as an experiment, with qualified product evidence: correction is possible, one-shot success is not demonstrated.

## Gate 10 — BMAD Adapter — 2026-08-28

### Objective
Make BMAD the first supported orchestrator through official customization while keeping the core independent.

### Implementation
Inspected and installed BMad Method 6.11.0, then added documented context/gate procedures, three sparse team overrides and a non-destructive `integrations install bmad` command. The overrides target the officially exposed architecture, build and code-review workflow fields.

### Functional and behavior tests
- real BMAD install: PASS, 49 Codex skills rendered;
- adapter installer into real BMAD tree: PASS;
- BMAD official customization resolver for 3 workflows: PASS;
- TOML parse validation: PASS;
- overwrite refusal and missing-install behavior: PASS;
- full suite: 57 passed;
- architecture gate: PASS.

### Metrics
- BMAD core dependencies: 0;
- official workflow overrides: 3;
- resolved override failures: 0;
- existing files silently overwritten: 0.

### Problems / negative results
The installed BMAD distribution requires `uv` to render `bmad-build` and `bmad-build-auto`; `uv` is not installed in the current environment. The adapter is structurally verified, but a real Build workflow is deferred to Gate 11.

### Status
PASS — pluggable adapter verified against BMAD 6.11.0; runtime E2E remains pending.

## Gate 11 — BMAD End-to-End Test — 2026-08-28

### Objective
Run a real BMAD Build→context→FAIL→correction→PASS→review workflow.

### Result
A real `$bmad-build` invocation rendered the customized workflow, loaded the harness persistent instruction, requested a 490-token architecture context, refreshed Graphify, propagated the expected gate FAIL and generated a 798-token spec. BMAD then correctly halted at its mandatory human approval checkpoint.

### Metrics
- real BMAD workflow runs: 1;
- override activation: PASS;
- compact context injection: PASS;
- FAIL propagation: PASS;
- implementation/correction/review stages: NOT_RUN;
- runner input tokens: 465219 (417280 cached);
- runner output tokens: 3859.

### Problems / negative results
Completing the workflow requires explicit human approval of the generated spec. The agent did not self-approve a human checkpoint. Therefore no BMAD correction success claim can be made.

### Status
PARTIAL — structurally and behaviorally proven through the approval boundary; post-approval E2E remains pending human action.

## Gate 12 — Generic / Codex / Claude Portability — 2026-08-28

### Objective
Prove that BMAD remains an adapter and the same public contract serves other agents.

### Implementation
Added requested Codex, Claude and generic adapters using the exact context, refresh and gate commands. Updated legacy snippets to the V2 checkpoint while retaining the V1.1 validate alias.

### Tests and metrics
- full suite: 59 passed;
- adapter contract parity: PASS for BMAD, Codex, Claude and generic;
- core imports of BMAD/Claude: 0;
- generic external subprocess contract test from Gate 4: PASS;
- current architecture gate: PASS.

### Problems / negative results
Only Codex has a real correction run in this environment. Claude portability is contract-tested but model execution is NOT_MEASURED because no Claude CLI is installed.

### Status
PASS for interface portability; cross-model behavior remains partially measured.

## Gate 13 — Optional ArchUnit Skill — 2026-08-28

### Objective
Offer code-level Java enforcement as an optional downstream module without coupling it to the macro harness.

### Implementation
Used the official skill-creator workflow to add `integrations/archunit`. It translates only human-confirmed validated rules, requires faithful relation/package mapping and keeps generated tests as review candidates.

### Tests and metrics
- official skill validation: PASS;
- full suite: 61 passed;
- core ArchUnit references/dependencies: 0;
- architecture gate: PASS;
- generated Java tests in this non-Java repository: 0.

### Problems / negative results
No Java fixture or native ArchUnit execution was added because this repository is Python and the module is intentionally optional. Runtime effectiveness is NOT_MEASURED.

### Status
PASS for external skill boundary; Java runtime behavior remains NOT_MEASURED.

## Gate 14 — A/B/C Benchmark — 2026-08-28

### Objective
Compare Graphify-only, Graphify-plus-full-architecture and compact Harness context on five identical tasks.

### Implementation and results
Added V2 benchmark mode, enriched applicable compact rules with severity/status/rationale, and ran all 15 context conditions with real Graphify queries for A/B. Detailed results are in `experiments/results/V2_ABC_BENCHMARK.md`.

### Metrics
- tasks: 5;
- A/B/C rows: 15;
- aggregate C versus B token reduction: 48.7%;
- Graphify calls A/B/C: 5 / 5 / 0;
- C assembly time: 0.0044–0.0047 seconds per task;
- task success and model output tokens: NOT_MEASURED.

### Problems / negative results
The benchmark measures context, not model performance. C selected up to 26 relevant files on the CLI task, and its benefit varies from 33.8% to 56.7% token reduction. No effectiveness claim is inferred from compression.

### Status
PASS for reproducible context benchmark; comparative model success remains NOT_MEASURED.

## Gate 15 — Final Evaluation — 2026-08-28

### Objective
Run the complete V2 validation and decide whether the evidence supports product use.

### Implementation
Promoted package metadata to 2.0.0, replaced the README with the detailed V2/BMAD workflow and principles, added `scripts/validate_v2.sh`, and produced `experiments/results/V2_FINAL_EVALUATION.md`.

### Final functional validation
- production Graphify refresh: PASS;
- normalized nodes / edges: 816 / 1369;
- freshness and doctor: PASS;
- pytest: 62 passed;
- architecture gate: PASS;
- capabilities contract: PASS;
- five-task A/B/C benchmark: PASS;
- Test Lab A–L: PASS;
- Rule Author and ArchUnit skills: PASS;
- BMAD override TOML: PASS.

### Final assessment
- software correctness: PASS;
- harness correctness: PASS on tested corpus, qualified;
- agent effectiveness: PARTIAL;
- BMAD integration: PARTIAL through mandatory approval boundary;
- portability: PASS at contract level;
- product usefulness: GO — HARNESS + CONTEXT.

### Problems / negative results
BMAD correction/review after spec approval, Claude execution, Java/ArchUnit execution, multi-task model success, and scaled maintenance cost remain NOT_MEASURED. V2 must not be sold as an unattended correctness guarantee.

### Status
PASS — V2 implementation complete with documented partial evidence where human/external execution remains outstanding.

## Gate 16 — Rule applicability and approved BMAD E2E — 2026-08-28

### Objective
Distinguish a real architecture violation from a rule that cannot yet be evaluated because Graphify did not observe one of its mapped elements, then continue the BMAD workflow through the human approval boundary.

### Implementation
- added explicit `required`, `when_observed`, and `declared_only` applicability to rules;
- added deterministic `PASS`, `FAIL`, `NOT_APPLICABLE`, and `UNRESOLVED` assessments;
- made a validated required rule with a missing Graphify mapping return `UNRESOLVED` and exit code 2 instead of a false violation;
- kept production validated rules strict with `required`, while candidate rules use `when_observed`;
- exposed assessments through the gate, JSON exporters, compact context, and agent capabilities;
- promoted package metadata to 2.1.0.

### Validation
- production Graphify refresh: PASS, 844 normalized nodes / 1426 edges;
- pytest: 65 passed;
- architecture gate: PASS, 8 / 8 rules evaluated PASS;
- capabilities, benchmark, Test Lab, skills, and BMAD overrides: PASS;
- approved BMAD E2E: PASS;
- runtime assertions: 2 / 2;
- BMAD review layers: 3 / 3;
- review findings corrected: 1 / 1;
- protected rule and Mermaid modifications: 0;
- final architecture gate in the generated project: PASS.

### Status
PASS — an absent Graphify identifier is now reported according to the rule's declared applicability, and the approved BMAD correction/review workflow has been exercised end to end once.

## Gate 17 — Official Mermaid and automatic Rule Author orchestration — 2026-08-28

### Objective
Install and invoke the Architecture Rule Author from each supported orchestrator, translate every official-parser-valid Mermaid source into retained facts and candidates, and resolve Mermaid-to-Graphify mappings without manual identifiers when evidence is sufficient.

### Implementation
- replaced the Python regex parser with a Node bridge backed by official Mermaid 11.17.2 and `@mermaid-js/parser`;
- added normalized graph extraction for flowchart, architecture, sequence, class, ER and state structures while retaining complete validated Mermaid source for every other family;
- added `arch-harness rules author-context --format json` with declared facts and ranked Graphify mapping evidence;
- revised `architecture-rule-author` to resolve evidence-backed mappings, defer greenfield mappings until code exists, and ask only about genuine semantic ambiguity or blocking promotion;
- made BMAD architecture/build invoke the installed skill automatically;
- added Codex and Claude installers that deploy the same skill plus project instructions;
- added the detailed cross-orchestrator manual guide in `documentation/INSTALLATION_ET_TEST_MANUEL.md`;
- promoted package metadata to 2.2.0.

### Validation
- skill validator: PASS;
- official Mermaid tests: flowchart, architecture-beta, sequence, class and ER PASS;
- BMAD, Codex and Claude isolated installation smoke tests: PASS;
- pytest: 68 passed;
- production Graphify: 899 normalized nodes / 1525 edges;
- V1 validation: PASS;
- V2 validation, production gate, benchmark, Test Lab, both skills and BMAD override parsing: PASS.

### Qualification
The official Mermaid parser validates all Mermaid-supported syntax, but diagram families without dependency-like semantics do not invent policy edges. Their complete source and extracted facts are retained for the LLM skill, which emits `declared_only` guidance or candidates. Only explicit human promotion can create blocking policy.

### Status
PASS — orchestrators now receive and invoke the Rule Author as an installed skill, mappings are proposed from real Graphify evidence, and Mermaid parsing is delegated to the official runtime.
