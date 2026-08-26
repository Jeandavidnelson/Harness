from architecture_harness.cache.manager import CacheManager


def test_cache_invalidates_only_when_input_changes(tmp_path):
    first = tmp_path / "first"
    second = tmp_path / "second"
    first.write_text("a")
    second.write_text("b")
    manager = CacheManager(tmp_path / "cache")
    manager.put("graph", [first], {"nodes": 1})
    manager.put("target", [second], {"nodes": 2})
    assert manager.get("graph", [first]) == {"nodes": 1}
    first.write_text("changed")
    assert manager.get("graph", [first]) is None
    assert manager.get("target", [second]) == {"nodes": 2}

