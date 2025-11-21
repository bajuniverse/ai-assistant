"""
Configuration loader for the AI assistant.

Loads configuration values from a YAML file (default `config.yaml` in the
project root). This module exposes a `Config` class that stores model,
retrieval, path, and logging settings.
"""

from pathlib import Path
import yaml

# Determine the default configuration file path relative to this module.
DEFAULT_CONFIG_PATH = Path(__file__).resolve().parents[1] / "config.yaml"


class Config:
    """Simple container for configuration data.

    The configuration is loaded from a YAML file. Unknown top-level keys
    will be ignored, but nested dictionaries for expected sections are
    preserved.
    """

    def __init__(self, path: Path | None = None) -> None:
        cfg_path = path or DEFAULT_CONFIG_PATH
        with open(cfg_path, "r", encoding="utf-8") as f:
            data = yaml.safe_load(f) or {}

        # Extract known sections, defaulting to empty dicts if missing.
        self.model: dict = data.get("model", {})
        self.rag: dict = data.get("rag", {})
        self.paths: dict = data.get("paths", {})
        self.logging: dict = data.get("logging", {})


def get_config(path: str | None = None) -> Config:
    """Load and return a Config object from the given path or the default.

    Args:
        path: Optional string path to a YAML file. If not provided, the
            default configuration location relative to this module will be used.

    Returns:
        Config: Loaded configuration.
    """
    return Config(Path(path) if path else None)