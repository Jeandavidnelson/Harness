from __future__ import annotations

from enum import Enum


class EvidenceOrigin(str, Enum):
    """Origin of an architectural fact, independent from extractor confidence."""

    DECLARED = "DECLARED"
    OBSERVED = "OBSERVED"
    INFERRED = "INFERRED"
    USER_CONFIRMED = "USER_CONFIRMED"
    GENERATED = "GENERATED"
    AMBIGUOUS = "AMBIGUOUS"


def origin_for_confidence(confidence: str) -> EvidenceOrigin:
    normalized = confidence.upper()
    if normalized == "INFERRED":
        return EvidenceOrigin.INFERRED
    if normalized == "AMBIGUOUS":
        return EvidenceOrigin.AMBIGUOUS
    if normalized in {"DECLARED", "DECLARED_CONTEXT"}:
        return EvidenceOrigin.DECLARED
    return EvidenceOrigin.OBSERVED
