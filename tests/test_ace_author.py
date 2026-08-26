import json
from pathlib import Path

from architecture_harness.ace.ape_adapter import validate_with_ape
from architecture_harness.ace.author import author_rule


ROOT = Path(__file__).parents[1]


def test_ace_corpus_never_hardens_ambiguity():
    corpus = json.loads((ROOT / "experiments" / "ace_rules.yaml").read_text())
    for case in corpus:
        result = author_rule(case["human_input"])
        assert result.status == case["expected_status"]
        assert result.intent == case["expected_intent"]
        assert result.ace == case["expected_ace"]
        if result.status != "EXACT":
            assert result.harness_rule is None


def test_exact_direct_and_transitive_mapping():
    direct = author_rule("Controllers must never call repositories directly.")
    assert direct.harness_rule["type"] == "forbidden_edge"
    transitive = author_rule("The domain must not depend on infrastructure.")
    assert transitive.harness_rule["type"] == "forbidden_path"


def test_ape_absence_is_nonfatal(tmp_path):
    path = tmp_path / "rule.ace"
    path.write_text("No controller may directly call a repository.")
    result = validate_with_ape(path)
    assert result["status"] in {"UNAVAILABLE", "AVAILABLE"}

