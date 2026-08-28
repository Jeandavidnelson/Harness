import json
from pathlib import Path

from architecture_harness.cli import main


ROOT = Path(__file__).parents[1]


def test_agent_capabilities_json(capsys):
    assert main(["--root", str(ROOT), "agent", "capabilities", "--format", "json"]) == 0
    payload = json.loads(capsys.readouterr().out)
    assert payload["api_version"] == "2.0"
    assert payload["llm_in_policy_engine"] is False


def test_top_level_capabilities_is_the_same_universal_contract(capsys):
    assert main(["--root", str(ROOT), "capabilities", "--format", "json"]) == 0
    payload = json.loads(capsys.readouterr().out)
    assert payload["commands"]["context"].startswith("arch-harness agent context")
    assert payload["commands"]["gate"] == "arch-harness gate --format json"
    assert payload["core_orchestrator_dependency"] is None


def test_agent_context_is_bounded_json(capsys):
    assert main(["--root", str(ROOT), "agent", "context", "--focus", "load_graphify", "--format", "json"]) == 0
    payload = json.loads(capsys.readouterr().out)
    assert set(payload) == {"observed_code", "declared_context", "target_architecture", "applicable_rules", "relevant_files", "provenance", "metrics"}
    assert payload["metrics"]["context_tokens"] > 0
    assert "nodes" not in payload


def test_agent_validate_and_doctor_json(capsys):
    assert main(["--root", str(ROOT), "agent", "validate", "--format", "json"]) == 0
    assert json.loads(capsys.readouterr().out)["status"] == "PASS"
    assert main(["--root", str(ROOT), "agent", "doctor", "--format", "json"]) == 0
    assert json.loads(capsys.readouterr().out)["status"] == "PASS"
