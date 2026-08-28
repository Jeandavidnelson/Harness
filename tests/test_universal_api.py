import json
import subprocess
from pathlib import Path


ROOT = Path(__file__).parents[1]
CLI = ROOT / ".venv" / "bin" / "arch-harness"


def test_generic_consumer_can_discover_and_request_context():
    capabilities = subprocess.run(
        [str(CLI), "--root", str(ROOT), "capabilities", "--format", "json"],
        check=True, capture_output=True, text=True,
    )
    contract = json.loads(capabilities.stdout)
    assert contract["api_version"] == "2.0"
    assert contract["exit_codes"] == {
        "pass": 0,
        "technical_error": 2,
        "unresolved": 2,
        "violation": 1,
    }

    context = subprocess.run(
        [str(CLI), "--root", str(ROOT), "agent", "context", "--focus", "cli", "--max-items", "5", "--format", "json"],
        check=True, capture_output=True, text=True,
    )
    payload = json.loads(context.stdout)
    assert payload["metrics"]["observed_edges"] <= 5
    assert payload["provenance"]["origins"]
