from pathlib import Path

import pytest

from architecture_harness.graphify_runtime import GraphifyRuntimeError, refresh_command, resolve_graphify


def test_refresh_uses_extract_without_manifest(tmp_path):
    graphify = tmp_path / "graphify"
    command = refresh_command(tmp_path, graphify)
    assert command == [str(graphify), "extract", str(tmp_path), "--code-only", "--no-cluster"]


def test_refresh_uses_incremental_update_with_manifest(tmp_path):
    output = tmp_path / "graphify-out"
    output.mkdir()
    (output / "manifest.json").write_text("{}")
    graphify = tmp_path / "graphify"
    assert refresh_command(tmp_path, graphify) == [str(graphify), "update", str(tmp_path), "--no-cluster"]


def test_missing_graphify_is_a_technical_error(tmp_path, monkeypatch):
    monkeypatch.setattr("architecture_harness.graphify_runtime.shutil.which", lambda _: None)
    with pytest.raises(GraphifyRuntimeError):
        resolve_graphify(tmp_path)

