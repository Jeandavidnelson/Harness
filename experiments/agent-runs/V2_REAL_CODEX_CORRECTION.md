# V2 Real Codex Correction Run

Date: 2026-08-28  
Runner: Codex CLI 0.146.0-alpha.9.2  
Project: isolated `/tmp/architecture-harness-v2-agent-loop`  
Execution kind: REAL_AGENT

## Prompt and context

The first prompt asked an independent Codex process to replace a direct Controller→Repository dependency with Controller→Service→Repository, using only the universal context, graph refresh and gate commands. Rules and Mermaid were immutable. The compact context contained 362 tokens, 6 observed edges, 2 relevant files and the applicable validated rule.

## Before

- Runtime: PASS before mutation.
- Graphify: 8 normalized nodes, 9 edges.
- Gate: FAIL with `controller-must-not-call-repository`.
- Evidence: controller and repository files, direct observed path, inferred provenance.

## Agent run 1

Actions observed: requested compact context, attempted a nonexistent service focus, read the gate, edited `src/controller.py`, refreshed Graphify twice and reran the gate.

Result:

- Gate: PASS.
- Runtime: FAIL because `service.py` did not exist.
- Files modified: `src/controller.py`.
- Usage reported by runner: 172,359 input tokens, 148,224 cached input tokens, 1,795 output tokens, 681 reasoning tokens.

Assessment: FAIL overall. A macro-architecture PASS did not imply functional correctness.

## Agent run 2

The follow-up could not resume because run 1 was ephemeral. A second independent process received the broken state and the explicit runtime failure. It added `src/service.py`, ran a runtime smoke test, refreshed Graphify and ran the gate.

Result:

- Runtime smoke test: PASS.
- Graphify: 13 normalized nodes, 16 edges initially.
- Gate with original experimental `forbidden_path`: FAIL because the intended Controller→Service→Repository path was transitively forbidden.
- Agent then moved repository construction to module scope; runtime and gate passed.
- Files modified: `src/service.py`.
- Usage reported by runner: 261,313 input tokens, 232,192 cached input tokens, 2,768 output tokens, 898 reasoning tokens.

Assessment: PARTIAL. The agent achieved both checks but optimized around a wrongly specified rule.

## Human analysis and correction

The rule rationale prohibited a direct dependency, while `forbidden_path` prohibited the intended layered path. The experimental rule was corrected to `forbidden_edge`; the unchanged application then passed both runtime and gate. This correction was not counted as an agent success.

## Metrics

| Metric | Value |
|---|---:|
| Real agent processes | 2 |
| Agent correction iterations | 2 |
| Initial architecture violation detected | yes |
| First-pass gate success | yes |
| First-pass task success | no |
| Final runtime + gate success | yes |
| Rule-model defect discovered | 1 |
| Silent rule modifications by agent | 0 |
| Wall duration | NOT_MEASURED |
| Tool call count | NOT_MEASURED |

## Conclusion

The real loop proves the CLI can steer an external agent from FAIL to PASS, but also falsifies any claim that the architecture gate alone guarantees working or high-quality code. Functional tests and correct rule semantics remain mandatory.
