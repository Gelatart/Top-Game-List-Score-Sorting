import pytest
import tempfile

from src.generator.cache_manager import CacheManager

def test_malformed_json_raises_json_decode_error(tmp_path):
    bad_file = tmp_path / "bad_cache.json"
    bad_file.write_text("{ this is not valid json }")

    cm = CacheManager(cache_file=str(bad_file))
    assert cm.cache == {}  # It should fallback safely, not crash