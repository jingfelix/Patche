import os
from functools import lru_cache

from pydantic_settings import BaseSettings


@lru_cache()
def get_settings():
    if not os.path.exists(Settings.Config.env_file):
        open(Settings.Config.env_file, "w").close()

    return Settings()


class Settings(BaseSettings):
    base_dir: str = "/home/laboratory/workspace/exps/ppatch"
    patch_store_dir: str = "_patches"
    max_diff_lines: int = 3

    class Config:
        env_file = os.path.join(os.environ.get("HOME"), ".ppatch.env")


settings = get_settings()
