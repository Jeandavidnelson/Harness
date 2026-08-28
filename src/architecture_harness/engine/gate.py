from __future__ import annotations

from architecture_harness.engine.harness import HarnessResult


def gate_payload(result: HarnessResult) -> dict[str, object]:
    """Return the stable checkpoint result. The gate never mutates project code."""
    blocking = [violation.to_dict() for violation in result.violations if violation.blocking]
    advisories = [violation.to_dict() for violation in result.violations if not violation.blocking]
    return {
        "status": result.status,
        "blocking": bool(blocking),
        "blocking_violations": blocking,
        "advisories": advisories,
        "rule_assessments": [item.to_dict() for item in result.assessments or []],
    }
