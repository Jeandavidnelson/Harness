from architecture_harness.ir.graph import Edge
from architecture_harness.ir.provenance import EvidenceOrigin


def test_all_v2_provenance_origins_are_explicit_and_stable():
    assert {item.value for item in EvidenceOrigin} == {
        "DECLARED", "OBSERVED", "INFERRED", "USER_CONFIRMED", "GENERATED", "AMBIGUOUS"
    }


def test_origin_is_distinct_from_extractor_confidence():
    edge = Edge("A", "B", provenance="EXTRACTED")
    assert edge.provenance == "EXTRACTED"
    assert edge.evidence_origin is EvidenceOrigin.OBSERVED

    generated = Edge("B", "C", provenance="LOW", origin=EvidenceOrigin.GENERATED)
    assert generated.provenance == "LOW"
    assert generated.evidence_origin is EvidenceOrigin.GENERATED
