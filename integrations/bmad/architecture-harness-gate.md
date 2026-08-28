# BMAD architecture checkpoint

At the end of a significant implementation step, story, epic, and before completion:

```bash
arch-harness graph refresh --format json
arch-harness gate --format json
```

- Exit 0 (`PASS` or non-blocking `WARN`): continue and retain advisories.
- Exit 1 (`FAIL`): inject the compact violation report into the current development workflow, correct code, refresh and rerun. Do not advance while a validated error remains.
- Exit 2 (`ERROR`): run `arch-harness doctor`; repair configuration or stale inputs before continuing.

Never weaken, delete or promote a rule merely to obtain PASS. If a validated rule is obsolete, stop for explicit human review and record the decision.
