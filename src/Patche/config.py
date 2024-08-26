import importlib.resources as pkg_resources
import os
from functools import lru_cache

from pydantic_settings import BaseSettings


@lru_cache()
def get_settings():
    _settings = Settings()
    if not os.path.exists(_settings.Config.env_file):
        open(_settings.Config.env_file, "w").close()

    return _settings


class Settings(BaseSettings):
    max_diff_lines: int = 3

    class Config:
        env_file = os.path.join(os.environ.get("HOME"), ".Patche.env")


settings = get_settings()
