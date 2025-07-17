from src.generator.config import check_for_src, get_env_var

class TestConfig:

    # def test_check_for_src_outside_src(monkeypatch): Try implementing?
    # def test_check_for_src_inside_src(monkeypatch): Try implementing?

    def test_get_env_var_missing_returns_empty(self):
        assert get_env_var("THIS_SHOULD_NOT_EXIST_123") == ""