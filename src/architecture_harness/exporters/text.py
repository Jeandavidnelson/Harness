from __future__ import annotations

from architecture_harness.engine.harness import HarnessResult


def render_text(result: HarnessResult) -> str:
    lines = ["ARCHITECTURE HARNESS", f"Result: {result.status}", "", f"Violations: {len(result.violations)}"]
    for violation in result.violations:
        lines.extend(["", f"[{violation.rule_id}]", "Observed:", " -> ".join(violation.observed_path), "", "Policy:", violation.policy])
        if violation.files or violation.provenance:
            lines.extend(["", "Evidence:"])
            lines.extend(violation.files)
            if violation.provenance:
                lines.append("provenance: " + ", ".join(violation.provenance))
    return "\n".join(lines)

