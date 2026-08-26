from __future__ import annotations

from architecture_harness.ir.context import CompactTaskContext


def render_llm_context(context: CompactTaskContext) -> str:
    lines = ["TASK FOCUS: " + ", ".join(context.focus), "", "Observed code:"]
    lines.extend(f"{e.source} -> {e.target} [{e.provenance}]" for e in context.observed_edges)
    lines.extend(["", "Declared runtime:"])
    lines.extend(f"{e.source} -> {e.target} [{e.provenance}; source={e.source_file}]" for e in context.context_edges)
    lines.extend(["", "Target architecture:"])
    lines.extend(f"{source} -> {target}" for source, target in context.target_edges)
    lines.extend(["", "Applicable rules:"])
    lines.extend(f"- {rule}" for rule in context.applicable_rules)
    lines.extend(["", "Relevant files:"])
    lines.extend(context.files)
    if context.truncated:
        lines.extend(["", "TRUNCATED: selection limits were reached"])
    return "\n".join(lines)

