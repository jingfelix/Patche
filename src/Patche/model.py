from enum import Enum
from typing import Optional

from pydantic import BaseModel
from whatthepatch.model import Change
from whatthepatch.model import Diff as WTPDiff
from whatthepatch.model import Header


class Line(BaseModel):
    index: int
    content: str
    changed: bool = False  # 标识在一轮 apply 中是否进行了修改
    status: bool = True  # 标识在一轮 apply 中是否被删除
    flag: bool = False  # 标识是否是在初次标记中修改了的行

    hunk: Optional[int] = None  # 如果 changed 为 True，则记录其所在的 hunk

    def __str__(self) -> str:
        return self.content


class File(object):
    def __init__(self, file_path: str) -> None:
        self.line_list: list[Line] = []

        with open(file_path, mode="r", encoding="utf-8") as f:
            for i, line in enumerate(f):
                self.line_list.append(Line(index=i, content=line.rstrip("\n")))

    def __str__(self) -> str:
        return "".join([str(line) for line in self.line_list])


class Hunk(BaseModel):
    index: int
    context: list[Change]
    middle: list[Change]
    post: list[Change]

    all_: list[Change]


class Diff(WTPDiff):
    hunks: list[Hunk]


class Patch(BaseModel):
    sha: str | None
    author: str | None
    date: str | None
    subject: str | None
    message: str | None
    diff: list[Diff] | list[WTPDiff] = []  # 临时的兼容方案


class ApplyResult(BaseModel):
    new_line_list: list[Line] = []
    conflict_hunk_num_list: list[int] = []
    failed_hunk_list: list[Hunk] = []


class CommandType(Enum):
    APPLY = "apply"
    AUTO = "auto"
    GET = "get"
    HELP = "help"
    SHOW = "show"
    TRACE = "trace"
    UNKNOWN = "unknown"


class CommandResult(BaseModel):
    type: CommandType
    content: dict | list | str | None = None
