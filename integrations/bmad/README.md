# BMAD 6.11 architecture-harness adapter

This adapter adds Architecture Harness checkpoints to BMAD without importing BMAD into the core. It was built against a real non-interactive BMad Method 6.11.0 installation and uses the official team override directory `_bmad/custom/`.

The adapter covers three workflow surfaces:

- `bmad-architecture`: turn Mermaid intent into reviewable candidate rules and require human promotion;
- `bmad-build`: request compact architectural context before implementation and require refresh/gate at meaningful checkpoints;
- `bmad-code-review`: load the latest architecture verdict and rerun the gate at review start.

Install and verify it using [install.md](install.md). The stable context instruction lives in [architecture-harness-context.md](architecture-harness-context.md), and FAIL handling in [architecture-harness-gate.md](architecture-harness-gate.md).

BMAD is the primary supported orchestrator, but all override instructions call the same public CLI used by other agents. The core has no BMAD dependency and never invokes BMAD itself.
