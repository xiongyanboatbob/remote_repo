"""配置管理器 - 管理应用程序的所有配置项"""

import json
import os
from pathlib import Path
from typing import Any

DEFAULT_CONFIG = {
    "ai": {
        "api_url": "https://api.openai.com/v1/chat/completions",
        "api_key": "",
        "model": "gpt-3.5-turbo",
        "max_tokens": 2048,
        "temperature": 0.7,
        "system_prompt": (
            "你是一个智能学习助手，帮助用户更高效地学习各种知识。"
            "请用简洁清晰的方式回答问题。"
        ),
    },
    "games": {
        "game_dirs": [],
        "custom_games": [],
    },
    "appearance": {
        "theme": "light",
        "font_size": 14,
        "language": "zh_CN",
    },
    "general": {
        "start_tab": 0,
        "auto_save_chat": True,
        "chat_history_limit": 100,
    },
}


class ConfigManager:
    """管理应用配置的读写"""

    def __init__(self) -> None:
        self._config_dir = Path.home() / ".config" / "smart-learner"
        self._config_file = self._config_dir / "config.json"
        self._config: dict[str, Any] = {}
        self._load()

    def _load(self) -> None:
        if self._config_file.exists():
            try:
                with open(self._config_file, "r", encoding="utf-8") as f:
                    saved = json.load(f)
                self._config = self._merge(DEFAULT_CONFIG, saved)
            except (json.JSONDecodeError, OSError):
                self._config = dict(DEFAULT_CONFIG)
        else:
            self._config = dict(DEFAULT_CONFIG)

    @staticmethod
    def _merge(default: dict, override: dict) -> dict:
        """递归合并配置，保留默认值中存在但覆盖中缺失的键"""
        result = dict(default)
        for key, value in override.items():
            if key in result and isinstance(result[key], dict) and isinstance(value, dict):
                result[key] = ConfigManager._merge(result[key], value)
            else:
                result[key] = value
        return result

    def save(self) -> None:
        os.makedirs(self._config_dir, exist_ok=True)
        with open(self._config_file, "w", encoding="utf-8") as f:
            json.dump(self._config, f, ensure_ascii=False, indent=2)

    def get(self, section: str, key: str, default: Any = None) -> Any:
        return self._config.get(section, {}).get(key, default)

    def set(self, section: str, key: str, value: Any) -> None:
        if section not in self._config:
            self._config[section] = {}
        self._config[section][key] = value

    def get_section(self, section: str) -> dict:
        return dict(self._config.get(section, {}))

    @property
    def config(self) -> dict:
        return self._config
