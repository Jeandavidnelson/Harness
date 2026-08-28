# V2 BMAD End-to-End Run

Date: 2026-08-28  
BMAD: 6.11.0  
uv: 0.12.7  
Runner: real Codex CLI process  
Status: PARTIAL — stopped at required human approval

## Executed path

1. Installed BMAD `bmm` and 49 Codex skills in the isolated correction project.
2. Installed the three Architecture Harness team overrides.
3. Introduced and verified a real Controller→Repository `forbidden_edge` violation.
4. Invoked `$bmad-build` with immutable Mermaid/rules and runtime acceptance criteria.
5. BMAD rendered the customized workflow through `uv run`.
6. The merged workflow loaded the harness checkpoint as a persistent fact and executed the appended compact-context instruction.
7. The agent requested context for `OrderController`: 490 tokens, 6 observed edges, 2 declared edges, 2 relevant files.
8. It refreshed Graphify and reproduced the blocking gate FAIL.
9. It generated a 798-token implementation spec.
10. BMAD halted at Checkpoint 1 and requested `[A] Approve | [E] Edit`.

## Assessment

Adapter activation, context injection, production Graphify and FAIL propagation are proven in a real BMAD workflow. Implementation, correction, PASS, and code-review handoff were not executed because BMAD reserves spec approval for the human. The outer execution request is not recorded as approval of this newly generated spec, so the run was not advanced automatically.

No success metric is claimed for the unexecuted part.
