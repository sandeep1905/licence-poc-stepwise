"""Loads config/rules.yaml and config/settings.yaml (cached)."""
import os
from functools import lru_cache
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent
CONFIG_DIR = ROOT / "config"


@lru_cache(maxsize=1)
def get_rules() -> dict:
    with open(CONFIG_DIR / "rules.yaml") as f:
        return yaml.safe_load(f)


@lru_cache(maxsize=1)
def get_settings() -> dict:
    with open(CONFIG_DIR / "settings.yaml") as f:
        s = yaml.safe_load(f)
    # an environment variable wins over the file
    if os.getenv("LLM_MODE"):
        s["llm_mode"] = os.environ["LLM_MODE"].lower()
    return s


def reload() -> None:
    """Clear the caches (used by tests that change the environment)."""
    get_rules.cache_clear()
    get_settings.cache_clear()
