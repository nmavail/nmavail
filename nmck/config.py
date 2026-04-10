import json
import os
from pathlib import Path

from dotenv import load_dotenv

# 尝试加载 .env 文件
load_dotenv()

CONFIG_FILE = Path.home() / ".config" / "namok" / "config.json"


class ConfigManager:
    def __init__(self):
        self.config_dir = Path.home() / ".config" / "namok"
        self.config_file = CONFIG_FILE
        self.data = self._load()

    def _load(self):
        if self.config_file.exists():
            try:
                with self.config_file.open() as f:
                    return json.load(f)
            except Exception:
                return {}
        return {}

    def save(self):
        self.config_dir.mkdir(parents=True, exist_ok=True)
        with self.config_file.open("w") as f:
            json.dump(self.data, f, indent=2)

    def get(self, key, default=None):
        # 优先级：环境变量 > 配置文件
        # 统一转为小写查找，防止键名大小写不一致
        env_val = os.getenv(key.upper())
        if env_val:
            return env_val.strip()
        return self.data.get(key.lower(), default)

    def set(self, key, value):
        self.data[key.lower()] = value
        self.save()


config_manager = ConfigManager()


class Config:
    @property
    def github_token(self):
        # 优先从环境变量获取，如果没有则尝试从配置管理器获取
        env_val = os.getenv("GITHUB_TOKEN")
        if env_val:
            return env_val
        return config_manager.get("github_token")

    @property
    def gitlab_token(self):
        env_val = os.getenv("GITLAB_TOKEN")
        if env_val:
            return env_val
        return config_manager.get("gitlab_token")
