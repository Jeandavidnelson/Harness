# Generic agent integration

Architecture Harness requires no SDK. A consumer needs process execution and JSON parsing only.

Discover the contract:

```bash
arch-harness capabilities --format json
```

Before implementation:

```bash
arch-harness agent context --focus <relevant-node> --format json
```

At meaningful checkpoints:

```bash
arch-harness graph refresh --format json
arch-harness gate --format json
```

Interpret exit 0 as non-blocking (`PASS` or `WARN`), 1 as a blocking validated architecture error, and 2 as a technical/configuration failure. On 1, give `blocking_violations` back to the coding agent and repeat after correction. On 2, run `arch-harness doctor`.

The consumer must not parse Mermaid itself, invent rules, modify code through the harness, or promote candidate rules automatically.
