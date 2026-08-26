from __future__ import annotations

from architecture_harness.engine.harness import HarnessResult


def render_markdown(result: HarnessResult) -> str:
    lines = ["# Architecture Harness", "", f"**Result: {result.status}**", "", f"Violations: {len(result.violations)}"]
    for violation in result.violations:
        lines.extend(["", f"## {violation.rule_id}", "", f"- Policy: `{violation.policy}`", f"- Observed: `{' -> '.join(violation.observed_path)}`"])
        if violation.files:
            lines.append(f"- Files: {', '.join(f'`{path}`' for path in violation.files)}")
        if violation.provenance:
            lines.append(f"- Provenance: {', '.join(violation.provenance)}")
    return "\n".join(lines)

