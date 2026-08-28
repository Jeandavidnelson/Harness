# Stable BMAD architecture context

Before significant implementation, identify the relevant Graphify node and run:

```bash
arch-harness agent context --focus <relevant-node> --format json
```

Give the resulting compact JSON to the implementing agent. Do not inject every Mermaid diagram or the full observed graph. Mermaid is declared guidance; only validated error rules can block.

For greenfield work, wait until meaningful code exists before the first Graphify refresh. For brownfield work, establish the Graphify baseline before development.
