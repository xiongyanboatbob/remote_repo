"""配置管理器测试"""

from pathlib import Path
from unittest.mock import patch

from smart_learner.config.config_manager import DEFAULT_CONFIG, ConfigManager


class TestConfigManager:
    def test_default_config_loaded(self, tmp_path: Path) -> None:
        config_dir = tmp_path / ".config" / "smart-learner"
        config_file = config_dir / "config.json"
        with patch.object(ConfigManager, "__init__", lambda self: None):
            mgr = ConfigManager()
            mgr._config_dir = config_dir
            mgr._config_file = config_file
            mgr._config = {}
            mgr._load()
        assert mgr.get("ai", "model") == "gpt-3.5-turbo"
        assert mgr.get("appearance", "theme") == "light"

    def test_set_and_get(self, tmp_path: Path) -> None:
        config_dir = tmp_path / ".config" / "smart-learner"
        config_file = config_dir / "config.json"
        with patch.object(ConfigManager, "__init__", lambda self: None):
            mgr = ConfigManager()
            mgr._config_dir = config_dir
            mgr._config_file = config_file
            mgr._config = dict(DEFAULT_CONFIG)
        mgr.set("ai", "model", "gpt-4")
        assert mgr.get("ai", "model") == "gpt-4"

    def test_save_and_reload(self, tmp_path: Path) -> None:
        config_dir = tmp_path / ".config" / "smart-learner"
        config_file = config_dir / "config.json"
        with patch.object(ConfigManager, "__init__", lambda self: None):
            mgr = ConfigManager()
            mgr._config_dir = config_dir
            mgr._config_file = config_file
            mgr._config = dict(DEFAULT_CONFIG)
        mgr.set("appearance", "font_size", 18)
        mgr.save()

        with patch.object(ConfigManager, "__init__", lambda self: None):
            mgr2 = ConfigManager()
            mgr2._config_dir = config_dir
            mgr2._config_file = config_file
            mgr2._config = {}
            mgr2._load()
        assert mgr2.get("appearance", "font_size") == 18

    def test_merge_preserves_defaults(self) -> None:
        default = {"a": {"x": 1, "y": 2}, "b": 3}
        override = {"a": {"x": 10}}
        result = ConfigManager._merge(default, override)
        assert result["a"]["x"] == 10
        assert result["a"]["y"] == 2
        assert result["b"] == 3

    def test_get_section(self, tmp_path: Path) -> None:
        config_dir = tmp_path / ".config" / "smart-learner"
        config_file = config_dir / "config.json"
        with patch.object(ConfigManager, "__init__", lambda self: None):
            mgr = ConfigManager()
            mgr._config_dir = config_dir
            mgr._config_file = config_file
            mgr._config = dict(DEFAULT_CONFIG)
        section = mgr.get_section("appearance")
        assert "theme" in section
        assert "font_size" in section
