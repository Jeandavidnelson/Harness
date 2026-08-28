from __future__ import annotations

import json

from architecture_harness.ir.context import CompactTaskContext
from architecture_harness.metrics.tokens import measure_tokens


def context_payload(context: CompactTaskContext) -> dict[str, object]:
    payload: dict[str, object] = {
        "observed_code": [
            {"source": edge.source, "target": edge.target, "relation": edge.relation, "provenance": edge.provenance, "origin": edge.evidence_origin.value}
            for edge in context.observed_edges
        ],
        "declared_context": [
            {"source": edge.source, "target": edge.target, "relation": edge.relation, "provenance": edge.provenance, "origin": edge.evidence_origin.value, "source_file": edge.source_file}
            for edge in context.context_edges
        ],
        "target_architecture": [{"source": source, "target": target} for source, target in context.target_edges],
        "applicable_rules": context.applicable_rules,
        "relevant_files": context.files,
        "provenance": {
            "observed": sorted({edge.provenance for edge in context.observed_edges}),
            "declared": sorted({edge.provenance for edge in context.context_edges}),
            "origins": sorted({edge.evidence_origin.value for edge in context.observed_edges + context.context_edges}),
        },
    }
    encoded = json.dumps(payload, sort_keys=True)
    measurement = measure_tokens(encoded)
    payload["metrics"] = {
        "context_tokens": measurement.count,
        "token_method": measurement.method,
        "observed_edges": len(context.observed_edges),
        "declared_edges": len(context.context_edges),
        "files": len(context.files),
        "truncated": context.truncated,
    }
    return payload


def render_agent_context(context: CompactTaskContext) -> str:
    return json.dumps(context_payload(context), indent=2, sort_keys=True)


def capabilities_payload() -> dict[str, object]:
    return {
        "api_version": "1.1",
        "commands": ["context", "validate", "doctor", "capabilities"],
        "formats": ["json"],
        "rule_types": ["required_edge", "forbidden_edge", "required_path", "forbidden_path"],
        "provenance": {
            "origins": ["DECLARED", "OBSERVED", "INFERRED", "USER_CONFIRMED", "GENERATED", "AMBIGUOUS"],
            "confidence": ["EXTRACTED", "INFERRED", "AMBIGUOUS", "DECLARED_CONTEXT"],
        },
        "exit_codes": {"pass": 0, "violation": 1, "technical_error": 2},
        "llm_in_policy_engine": False,
    }
