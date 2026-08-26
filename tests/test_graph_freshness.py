import hashlib
import json

from architecture_harness.graph_freshness import check_graph_freshness


def test_stale_graph_is_not_silently_accepted(tmp_path):
    source = tmp_path / "src" / "module.py"
    source.parent.mkdir()
    source.write_text("VALUE = 1\n")
    output = tmp_path / "graphify-out"
    output.mkdir()
    digest = hashlib.md5(source.read_bytes()).hexdigest()
    (output / "manifest.json").write_text(json.dumps({"src/module.py": {"ast_hash": digest}}))
    assert check_graph_freshness(tmp_path).fresh
    source.write_text("VALUE = 2\n")
    result = check_graph_freshness(tmp_path)
    assert not result.fresh
    assert result.stale_files == ("src/module.py",)


def test_new_source_missing_from_manifest_is_stale(tmp_path):
    (tmp_path / "src").mkdir()
    (tmp_path / "src" / "new.py").write_text("pass\n")
    output = tmp_path / "graphify-out"
    output.mkdir()
    (output / "manifest.json").write_text("{}")
    assert check_graph_freshness(tmp_path).missing_files == ("src/new.py",)

