from __future__ import annotations

from dataclasses import asdict, dataclass


@dataclass(frozen=True)
class Violation:
    rule_id: str
    policy: str
    source: str
    target: str
    observed_path: tuple[str, ...]
    files: tuple[str, ...] = ()
    provenance: tuple[str, ...] = ()
    severity: str = "error"
    rule_status: str = "validated"
    rationale: str = ""
    expected_architecture: str = ""

    @property
    def blocking(self) -> bool:
        return self.severity == "error" and self.rule_status == "validated"

    def to_dict(self) -> dict[str, object]:
        data = asdict(self)
        data["observed_path"] = list(self.observed_path)
        data["files"] = list(self.files)
        data["provenance"] = list(self.provenance)
        return data
