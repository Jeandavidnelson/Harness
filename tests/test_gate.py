import hashlib
import json
from pathlib import Path

from architecture_harness.cli import main
from architecture_harness.engine.gate import gate_payload
from architecture_harness.engine.harness import HarnessResult
from architecture_harness.engine.violations import Violation


ROOT = Path(__file__).parents[1]


def test_gate_payload_has_stable_pass_and_fail_states():
    assert gate_payload(HarnessResult([])) == {
        "status": "PASS", "blocking": False, "blocking_violations": [], "advisories": []
    }
    violation = Violation("r1", "forbidden_edge", "A", "B", ("A", "B"))
    payload = gate_payload(HarnessResult([violation]))
    assert payload["status"] == "FAIL"
    assert payload["blocking"] is True
    assert payload["blocking_violations"][0]["rule_id"] == "r1"


def test_gate_is_read_only_and_returns_machine_contract(capsys):
    tracked = ROOT / "src" / "architecture_harness" / "ir" / "rules.py"
    before = hashlib.sha256(tracked.read_bytes()).hexdigest()
    assert main(["--root", str(ROOT), "gate", "--format", "json"]) == 0
    payload = json.loads(capsys.readouterr().out)
    assert payload["status"] == "PASS"
    assert payload["blocking"] is False
    assert hashlib.sha256(tracked.read_bytes()).hexdigest() == before
