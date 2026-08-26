from __future__ import annotations

from dataclasses import dataclass, field


RULE_TYPES = {"required_edge", "forbidden_edge", "required_path", "forbidden_path"}


@dataclass(frozen=True)
class MatchSpec:
    exact: str | None = None
    suffix: str | None = None
    prefix: str | None = None
    contains: str | None = None


@dataclass(frozen=True)
class Rule:
    id: str
    type: str
    source: str
    target: str
    allowed_targets: tuple[str, ...] = ()


@dataclass
class RulesIR:
    roles: dict[str, MatchSpec] = field(default_factory=dict)
    rules: list[Rule] = field(default_factory=list)

