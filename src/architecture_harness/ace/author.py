from __future__ import annotations

import re
from dataclasses import asdict, dataclass


WARNING = re.compile(r"\b(should|normally|generally|preferably|when appropriate|where possible|if necessary|typically|ideally|recommended|avoid|usually|when useful)\b", re.I)


@dataclass(frozen=True)
class AceAuthoringResult:
    original: str
    intent: str
    status: str
    ace: str | None
    structured: dict[str, object] | None
    assumptions: tuple[str, ...]
    harness_rule: dict[str, str] | None
    role_resolution: str
    reason: tuple[str, ...]

    def to_dict(self) -> dict[str, object]:
        result = asdict(self)
        result["assumptions"] = list(self.assumptions)
        result["reason"] = list(self.reason)
        return result


def _exact(original: str, intent: str, ace: str, source: str, relation: str, direct: bool, target: str, policy: str, rule_type: str | None) -> AceAuthoringResult:
    harness = {"type": rule_type, "source": source.title().replace(" ", ""), "target": target.title().replace(" ", "")} if rule_type else None
    return AceAuthoringResult(original, intent, "EXACT", ace, {
        "source_role": source, "relation": relation, "direct": direct,
        "target_role": target, "policy": policy,
    }, (), harness, "REQUIRED", ())


def author_rule(text: str) -> AceAuthoringResult:
    original = text.strip()
    if not original:
        return AceAuthoringResult(original, "UNKNOWN", "UNSUPPORTED", None, None, (), None, "REQUIRED", ("empty rule",))
    warnings = WARNING.findall(original)
    if warnings:
        return AceAuthoringResult(original, "UNKNOWN", "NEEDS_CLARIFICATION", None, None, (), None, "REQUIRED", tuple(f'advisory or conditional term: "{word}"' for word in warnings))
    normalized = re.sub(r"[.!]$", "", original.lower()).strip()
    if normalized in {
        "no controller may directly call a repository",
        "controllers must never call repositories directly",
        "controllers must not directly call repositories",
        "les controllers ne doivent jamais appeler directement les repositories",
    }:
        return _exact(original, "FORBID", "No controller may directly call a repository.", "controller", "calls", True, "repository", "forbidden", "forbidden_edge")
    if normalized in {"every repository may access a database", "repositories may access databases"}:
        return _exact(original, "ALLOW", "Every repository may access a database.", "repository", "accesses", True, "database", "allowed", None)
    if normalized in {
        "no domain component may depend on infrastructure",
        "no domain component may depend on an infrastructure component",
        "the domain must not depend on infrastructure",
    }:
        return _exact(original, "FORBID", "No domain component may depend on an infrastructure component.", "domain", "depends_on", False, "infrastructure", "forbidden", "forbidden_path")
    if normalized in {"external payment calls must pass through the payment gateway", "external payment calls must pass through a gateway"}:
        return _exact(original, "REQUIRE", "Every external payment call must pass through the payment gateway.", "external payment call", "passes_through", False, "payment gateway", "required", "required_path")
    if " and " in normalized or ";" in normalized:
        reason = "compound rules must be split into independent constraints"
    else:
        reason = "relation or modality is outside the deterministic V1.1 authoring corpus"
    return AceAuthoringResult(original, "UNKNOWN", "UNSUPPORTED", None, None, (), None, "REQUIRED", (reason,))

