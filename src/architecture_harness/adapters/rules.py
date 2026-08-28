from __future__ import annotations

from pathlib import Path

from architecture_harness.ir.rules import RULE_APPLICABILITY, RULE_SEVERITIES, RULE_STATUSES, RULE_TYPES, MatchSpec, Rule, RulesIR


class RulesError(ValueError):
    pass


def _value(text: str):
    value = text.strip()
    if not value:
        return ""
    if value.startswith("[") and value.endswith("]"):
        return [item.strip().strip("'\"") for item in value[1:-1].split(",") if item.strip()]
    return value.strip("'\"")


def load_rules(path: str | Path) -> RulesIR:
    """Parse the deliberately small, explicit YAML subset used by V1."""
    source = Path(path)
    try:
        lines = source.read_text(encoding="utf-8").splitlines()
    except OSError as exc:
        raise RulesError(f"Cannot read rules {source}: {exc}") from exc
    result = RulesIR()
    section = None
    role = None
    current: dict[str, object] | None = None
    for number, raw in enumerate(lines, 1):
        content = raw.split("#", 1)[0].rstrip()
        if not content.strip():
            continue
        indent = len(content) - len(content.lstrip())
        text = content.strip()
        if indent == 0 and text in ("roles:", "rules:"):
            if current:
                result.rules.append(_make_rule(current, source, number))
                current = None
            section = text[:-1]
            role = None
            continue
        if section == "roles":
            if indent == 2 and text.endswith(":"):
                role = text[:-1]
                result.roles[role] = MatchSpec()
            elif indent >= 6 and ":" in text and role:
                key, raw_value = text.split(":", 1)
                if key not in {"exact", "suffix", "prefix", "contains"}:
                    raise RulesError(f"{source}:{number}: unsupported matcher {key}")
                values = result.roles[role].__dict__ | {key: str(_value(raw_value))}
                result.roles[role] = MatchSpec(**values)
            elif text != "match:":
                raise RulesError(f"{source}:{number}: invalid roles syntax")
        elif section == "rules":
            if text.startswith("- "):
                if current:
                    result.rules.append(_make_rule(current, source, number))
                current = {}
                text = text[2:].strip()
            if current is not None and ":" in text:
                key, raw_value = text.split(":", 1)
                current[key] = _value(raw_value)
            else:
                raise RulesError(f"{source}:{number}: invalid rule syntax")
        else:
            raise RulesError(f"{source}:{number}: expected roles: or rules:")
    if current:
        result.rules.append(_make_rule(current, source, len(lines)))
    if not result.rules:
        raise RulesError("At least one rule is required")
    return result


def _make_rule(data: dict[str, object], source: Path, number: int) -> Rule:
    missing = {"id", "type", "source", "target"} - data.keys()
    if missing:
        raise RulesError(f"{source}:{number}: missing rule fields: {', '.join(sorted(missing))}")
    if data["type"] not in RULE_TYPES:
        raise RulesError(f"{source}:{number}: unsupported rule type {data['type']}")
    severity = str(data.get("severity", "error"))
    status = str(data.get("status", "validated"))
    applicability = str(data.get("applicability", "required"))
    if severity not in RULE_SEVERITIES:
        raise RulesError(f"{source}:{number}: unsupported severity {severity}")
    if status not in RULE_STATUSES:
        raise RulesError(f"{source}:{number}: unsupported status {status}")
    if applicability not in RULE_APPLICABILITY:
        raise RulesError(f"{source}:{number}: unsupported applicability {applicability}")
    allowed = data.get("allowed_targets", [])
    if isinstance(allowed, str):
        allowed = [allowed]
    scope = data.get("scope", [])
    if isinstance(scope, str):
        scope = [scope]
    exceptions = data.get("exceptions", [])
    if isinstance(exceptions, str):
        exceptions = [exceptions]
    return Rule(
        str(data["id"]), str(data["type"]), str(data["source"]), str(data["target"]), tuple(allowed),
        severity, tuple(scope), tuple(exceptions), str(data.get("rationale", "")),
        str(data.get("provenance", "USER_CONFIRMED")), status, applicability,
    )
