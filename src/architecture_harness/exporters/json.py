from __future__ import annotations

import json

from architecture_harness.engine.harness import HarnessResult


def render_json(result: HarnessResult) -> str:
    return json.dumps({
        "status": result.status,
        "blocking": any(v.blocking for v in result.violations),
        "violations": [v.to_dict() for v in result.violations],
        "rule_assessments": [item.to_dict() for item in result.assessments or []],
    }, indent=2)
