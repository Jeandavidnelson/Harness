from architecture_harness.cli import main


def test_observed_command(capsys, tmp_path):
    output = tmp_path / "graphify-out"
    output.mkdir()
    (output / "graph.json").write_text('{"nodes": [{"id": "A"}], "edges": []}')
    assert main(["--root", str(tmp_path), "observed"]) == 0
    assert "nodes: 1" in capsys.readouterr().out

