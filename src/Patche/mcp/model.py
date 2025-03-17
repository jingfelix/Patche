from enum import Enum

from pydantic import BaseModel


# 定义 Patche 相关的数据模型
class PatcheConfig(BaseModel):
    pass


class PatcheList(BaseModel):
    patche_dir: str


class PatcheShow(BaseModel):
    patch_path: str


class PatcheApply(BaseModel):
    patch_path: str
    target_dir: str
    reverse: bool = False


class PatcheTools(str, Enum):
    CONFIG = "patche_config"
    LIST = "patche_list"
    SHOW = "patche_show"
    APPLY = "patche_apply"
