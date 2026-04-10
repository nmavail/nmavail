import json
from pathlib import Path

from dotenv import load_dotenv

# Try to load .env file
load_dotenv()

CONFIG_FILE = Path.home() / ".config" / "nmck" / "config.json"

# Global timeout setting (in seconds)
DEFAULT_TIMEOUT = 10.0  # Default timeout for all HTTP requests


class ConfigManager:
    def __init__(self):
        self.config_dir = Path.home() / ".config" / "nmck"
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
        # Get token only from config file
        return self.data.get(key.lower(), default)

    def set(self, key, value):
        self.data[key.lower()] = value
        self.save()


config_manager = ConfigManager()


class Config:
    @property
    def github_token(self):
        # Get GitHub token from config file
        return config_manager.get("github_token")

    @property
    def gitlab_token(self):
        # Get GitLab token from config file
        return config_manager.get("gitlab_token")
