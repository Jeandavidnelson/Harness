# V2 Agent Behavior Log

## 2026-08-28 — Real Codex correction loop

- Two independent ephemeral Codex CLI processes ran against an isolated project.
- Run 1 consumed compact harness context and removed the direct repository dependency, but invented an absent service module: gate PASS, runtime FAIL.
- Run 2 added the service and passed runtime, then encountered the incorrect transitive policy and altered dependency construction to obtain gate PASS.
- No agent changed Mermaid or validated rules.
- Human assessment found one rule-model defect (`forbidden_path` versus intended `forbidden_edge`).
- Final state after correcting the experimental rule: runtime PASS and gate PASS.
- Evidence: `experiments/agent-runs/V2_REAL_CODEX_CORRECTION.md`.
