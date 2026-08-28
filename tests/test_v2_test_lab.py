import importlib.util
from pathlib import Path


ROOT = Path(__file__).parents[1]
SPEC = importlib.util.spec_from_file_location("v2_lab", ROOT / "experiments" / "run_v2_test_lab.py")
MODULE = importlib.util.module_from_spec(SPEC)
assert SPEC.loader
SPEC.loader.exec_module(MODULE)


def test_all_v2_lab_scenarios_are_reproducible_and_honest():
    result = MODULE.run_lab()
    assert [case["id"] for case in result["cases"]] == list("ABCDEFGHIJKL")
    assert all(case["execution_kind"] == "DETERMINISTIC_SIMULATION" for case in result["cases"])
    assert result["summary"]["detection_rate"] == 1.0
    assert result["summary"]["false_blocking_rate"] == 0.0
    assert result["summary"]["real_agent_runs"] == 0


def test_adversarial_and_candidate_behavior():
    cases = {case["id"]: case for case in MODULE.run_lab()["cases"]}
    assert cases["B"]["harness_verdict"]["initial"]["status"] == "FAIL"
    assert cases["B"]["harness_verdict"]["final"]["status"] == "PASS"
    assert cases["E"]["harness_verdict"]["candidate"]["status"] == "WARN"
    assert cases["E"]["harness_verdict"]["validated"]["status"] == "FAIL"
    assert cases["I"]["harness_verdict"]["status"] == "PASS"
