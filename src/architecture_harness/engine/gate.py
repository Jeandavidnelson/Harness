from __future__ import annotations

from architecture_harness.engine.harness import HarnessResult


def gate_payload(result: HarnessResult) -> dict[str, object]:
    """Return the stable checkpoint result. The gate never mutates project code."""
    violations = [violation.to_dict() for violation in result.violations]
    return {
        "status": "FAIL" if violations else "PASS",
        "blocking": bool(violations),
        "blocking_violations": violations,
        "advisories": [],
    }
