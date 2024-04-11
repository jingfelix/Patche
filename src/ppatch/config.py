import importlib.resources as pkg_resources
import os
from functools import lru_cache

from pydantic_settings import BaseSettings


@lru_cache()
def get_settings():
    _settings = Settings()
    if not os.path.exists(_settings.Config.env_file):
        open(_settings.Config.env_file, "w").close()

    patch_store_path = os.path.join(_settings.base_dir, _settings.patch_store_dir)
    if not os.path.exists(patch_store_path):
        os.makedirs(patch_store_path)

    return _settings


class Settings(BaseSettings):
    base_dir: str = str(pkg_resources.files("ppatch"))
    patch_store_dir: str = "_patches"
    max_diff_lines: int = 3

    class Config:
        env_file = os.path.join(os.environ.get("HOME"), ".ppatch.env")


settings = get_settings()
