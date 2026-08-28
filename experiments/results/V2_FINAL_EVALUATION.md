# Architecture Harness V2 — Final Evaluation

Date: 2026-08-28  
Branch: `feat/architecture-harness-v2`

## Decision

**GO — HARNESS + CONTEXT**, with BMAD post-approval E2E explicitly incomplete.

V2 is suitable as a deterministic architecture guidance and feedback module for controlled use. It is not yet justified as an unattended guarantee of autonomous-agent success.

## 1. Software correctness

PASS. The final validation exercises Graphify refresh/freshness, configuration, 62+ tests, the universal gate, capability discovery, Test Lab, benchmark, two skills and BMAD TOML. The exact final count is recorded by `scripts/validate_v2.sh`.

Known limitation: role mapping can still be semantically empty if a declared matcher resolves no observed node; production rules need resolution tests.

## 2. Harness correctness

PASS on the tested corpus, qualified. The deterministic A–L lab detected 4/4 known violations and produced zero false blocking on the included legitimate cases. Candidate and warning findings do not block; only validated errors do. Ambiguous evidence does not hard-fail.

This is corpus evidence, not a universal 100% claim. The real-agent experiment discovered one incorrect `forbidden_path` policy, showing that rule authoring can itself introduce friction or gaming.

## 3. Agent effectiveness

PARTIAL. Two real Codex processes took one isolated task from architecture FAIL to final runtime+gate PASS. The first process reached gate PASS while leaving a missing module, proving the gate cannot replace functional verification. The second reacted to a bad transitive rule by changing code shape around the graph. One task is insufficient for a success rate.

## 4. BMAD integration

PARTIAL/PASS THROUGH APPROVAL BOUNDARY. BMAD 6.11.0 was really installed. Three official team overrides were resolved by BMAD's own resolver. A real `$bmad-build` loaded the compact-context instruction, received a 490-token context, refreshed Graphify, propagated FAIL and generated a spec. It halted at the required human approval; correction/PASS/review were not run.

The core contains no BMAD dependency.

## 5. Portability

PASS at contract level. BMAD, Codex, Claude and generic adapters share the same CLI. A generic subprocess and Codex were executed. Claude runtime behavior is `NOT_MEASURED` because no Claude CLI was installed.

## 6. Product usefulness

PROMISING AND QUALIFIED. Compact context reduced tokens by 48.7% against Graphify plus full architecture on five repository tasks. The rule lifecycle prevents silent LLM policy promotion, and violation evidence was actionable in real runs.

Costs and friction remain material: human clarification and maintenance costs are not measured at scale; exact mappings require care; a wrong edge/path choice can block intended layering; Graphify output grows when orchestrator files are present.

## Acceptance criteria assessment

| Criterion | Result |
|---|---|
| Production Graphify, not reimplementation | PASS |
| Mermaid guides without automatic blocking | PASS |
| Only validated errors hard-fail | PASS |
| Universal CLI and exit codes | PASS |
| Core independent from BMAD | PASS |
| Real agent correction evidence | PASS, one qualified task |
| Real BMAD E2E through review | PARTIAL |
| Cross-model proof | NOT_MEASURED |
| Maintenance cost measured | PARTIAL, one synthetic evolution only |

## Final answer

Architecture Harness reliably supplies compact, provenance-aware guidance and deterministic feedback to BMAD and other agents on the exercised cases without coupling the core to orchestration. Evidence is not yet sufficient to claim reliable unattended preservation across projects: human rule validation, functional tests, code review, and completion of the BMAD post-approval workflow remain necessary.

Recommended next milestone: obtain explicit approval for the generated BMAD spec, finish Build→PASS→code-review, then repeat matched real-agent tasks across Java and a second language while measuring clarification and rule-maintenance cost.
