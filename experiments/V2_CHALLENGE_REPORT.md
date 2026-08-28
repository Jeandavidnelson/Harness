# V2 Challenge Report

Date: 2026-08-28  
Baseline commit inspected: `0231c3d`  
Branch: `feat/architecture-harness-v2`

## Decision

**PROCEED WITH CHANGES**

Proceed only if V2 is treated as an architecture-guidance and validated-policy engine with BMAD as its first adapter. Do not position it as a universal replacement for native architecture tests, do not infer blocking constraints from Mermaid arrows, and do not claim agent effectiveness until real workflow evidence exists.

## Falsification criteria

V2 should stop or redesign if any of the following remains true after the Test Lab:

- candidate or inferred rules can block code;
- unresolved role mappings pass silently at the Gate;
- known violations are detected below 90%;
- false blocking exceeds 10% in the defined corpus;
- correction succeeds below 80%;
- BMAD integration requires a core dependency or a BMAD fork;
- compact context loses information required for the defined agent tasks;
- rule maintenance requires repeated manual identifier repair after ordinary refactors.

## 1. Incremental value versus Graphify alone

### Evidence for value

Graphify observes topology and provenance but does not know which dependencies are policies. V1.1 adds explicit required/forbidden edge/path rules, stable exit codes, compact violation reports, freshness checks and task-focused context. Its final benchmark recorded 46.2% context reduction versus Graphify plus full architecture.

### Evidence against value

The V1.1 A/B/C benchmark did not measure model task success, output tokens or total tokens. The correction tests mutate the observed graph in memory; they do not prove that an autonomous agent uses the feedback correctly. Graphify already offers scoped queries, so context reduction alone is insufficient product differentiation.

### Challenge conclusion

Incremental value is plausible only for validated policies, normalized multi-validator evidence and orchestration-friendly guidance. It is unproven for agent effectiveness.

## 2. Mermaid as macro architecture

Mermaid is effective for components, directions, subgraphs and external context. It is readable by architects and agents and remains technology-neutral.

It is insufficient to express modality, exceptions, scope, severity, relation semantics or whether absence of an arrow means forbidden. V1.1 correctly avoids interpreting arrows as MUST/MUST NOT, but it also means the declared target graph currently contributes little to blocking evaluation beyond role/subgraph resolution and context projection.

**Required change:** preserve Mermaid as guidance; place executable meaning in reviewed rules and report undeclared drift only as non-blocking evidence unless a validated rule exists.

## 3. False positives and false negatives

V1.1 reports 0 false positives and 0 false negatives only within eight targeted in-memory mutations. This is not representative of Graphify extraction uncertainty or agent-generated repositories.

Identified false-positive risks:

- `forbidden_edge` does not filter `relation`, so `imports`, `uses`, `references` and `calls` are equivalent;
- exact Graphify IDs can change after refactors or extractor upgrades;
- transitive paths may pass through utility/test nodes irrelevant to the intended scope;
- context-declared edges could be mistaken for observed evidence by a consumer despite provenance fields.

Identified false-negative risks:

- a rule whose source role resolves to zero nodes produces no violation;
- missing Graphify edges are invisible to the harness;
- `AMBIGUOUS` edges never hard-fail, which is safe but can hide a real dependency;
- target Mermaid arrows are not executable unless backed by rules;
- allowed-target semantics are incomplete and not scoped by relation.

**Required change:** add explicit mapping diagnostics, relation/scope support, rule lifecycle and Test Lab coverage using real extracted graphs.

## 4. Rule maintenance cost

V1.1 uses nine exact mappings for eight rules. This is precise but brittle. No metric currently measures time or edits needed after renaming components, changing Mermaid, upgrading Graphify or evolving architecture.

**Required experiment:** record rules edited, mappings edited, clarification count and elapsed maintenance time in architecture-evolution scenarios. Use stable logical roles where possible; never silently remap exact IDs.

## 5. User questions

The ACE experiment rejects three ambiguous phrases but does not implement an interactive clarification lifecycle. No current metric records question count or resolution latency.

Questions must be limited to decisions that change enforcement, such as:

- Is an arrow guidance, allowed direction or required dependency?
- Is a dependency direct or transitive?
- Does the rule apply globally, to one service, or to production code only?
- Is the outcome warning or blocking?
- Are logging, metrics and tests exceptions?

The system should group questions and avoid asking about facts derivable from deterministic graphs.

## 6. Appropriate checkpoints

Running after every file would create friction and Graphify churn. Running only at sprint end permits expensive drift.

Recommended checkpoints:

1. after a meaningful vertical slice;
2. at story/task completion;
3. before code review;
4. in CI;
5. at epic end for global drift and rule maintenance review.

Greenfield projects should not run Graphify before meaningful code exists. Brownfield projects require a baseline before development.

## 7. Blocking versus warning

V1.1 has binary rule behavior. That is too coarse for Mermaid guidance and inferred candidates.

Required behavior:

- `error + validated` may block;
- `warning + validated` reports without exit code 1;
- `info` is advisory;
- `candidate`, `proposed`, `clarification`, `inferred` and `ambiguous` never block;
- stale or invalid configuration returns technical exit code 2, not architectural FAIL.

## 8. Provenance separation

V1.1 preserves `EXTRACTED`, `INFERRED`, `AMBIGUOUS` and `DECLARED_CONTEXT`, which is a strong base. V2 needs a clearer distinction between fact origin and confidence level:

- `DECLARED`: deterministic Mermaid fact;
- `OBSERVED`: normalized Graphify fact;
- `INFERRED`: LLM or resolution inference;
- `USER_CONFIRMED`: explicit human decision;
- `GENERATED`: machine-produced candidate/test;
- `AMBIGUOUS`: unresolved evidence.

Provenance must be attached to rules, paths, reports and generated artifacts. It must not be encoded only in display text.

## 9. BMAD independence

The current core imports no BMAD code. The V1.1 BMAD integration is documentation-only and therefore independent, but it is not a tested integration.

**Required change:** keep the CLI as the only engine contract. Generate BMAD customization files through an adapter after inspecting an actual BMAD installation. Never copy the engine into `_bmad/` or fork installed workflows.

## 10. Portability

The universal JSON commands and exit codes support portability in principle. Existing Claude/Codex/BMAD documents call the same CLI. There is no generic adapter test against a clean consumer project.

**Required experiment:** run a generic-agent scenario using only capabilities, context and validate commands, without repository-specific instructions.

## 11. ArchUnit as an external module

ArchUnit adds bytecode-level Java semantics, layers, cycles, annotations and richer conditions that the macro graph should not reproduce. It is valuable as an optional generator/validator adapter.

Risks are duplicated policy, conflicting evidence and auto-generated invariants becoming permanent without review.

**Required boundary:** ArchUnit tests are generated as candidates, require human validation, and report independent L4 evidence. The core must run without Java or ArchUnit.

## 12. Product scope after challenge

### Keep

- Graphify adapter and freshness protection;
- deterministic Mermaid and context parsing;
- compact agent API;
- deterministic edge/path evaluation;
- provenance preservation;
- orchestration-independent CLI.

### Change before claiming V2

- add status, severity, scope, exceptions, rationale and provenance to rules;
- ensure only validated errors block;
- distinguish warning, fail and technical error;
- expose universal graph refresh, gate and capabilities commands;
- implement candidate promotion with explicit human action;
- test real extracted projects and real agent behavior;
- package BMAD as an adapter using official customization surfaces.

### Defer or reject

- automatic blocking-rule derivation from Mermaid;
- LLM verdicts;
- automatic ArchUnit invariant promotion;
- custom MCP requirement;
- multi-agent runtime;
- ontology or vector database.

## Final challenge answer

The hypothesis is not yet proven. V1.1 demonstrates a functioning deterministic graph-policy core, but not reliable BMAD or autonomous-agent improvement. V2 may proceed with a narrower claim: it can provide architectural guidance and enforce only human-validated rules through a portable CLI. The Test Lab and BMAD end-to-end gates must earn any stronger product claim.

