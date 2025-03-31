import re
from typing import Iterator, Optional

from Patche.model import Header

HEADER_OLD = re.compile(r"^--- ([^\t\n]+)(?:\t([^\n]*)|)$")
HEADER_NEW = re.compile(r"^\+\+\+ ([^\t\n]+)(?:\t([^\n]*)|)$")
HUNK_START = re.compile(r"^@@ -(\d+)(?:,(\d+))? \+(\d+)(?:,(\d+))? @@")
CHANGE_LINE = re.compile(r"^([- +\\])(.*)$")
GIT_HEADER = re.compile(r"^diff --git a/(.*) b/(.*)$")


def parse_header(lines: Iterator[str]) -> Optional[Header]:
    """解析 diff 头部信息"""

    old_line = next(lines, "")
    new_line = next(lines, "")

    if GIT_HEADER.match(old_line):
        old_line = next(lines, "")
        new_line = next(lines, "")

    old_match = HEADER_OLD.match(old_line)
    new_match = HEADER_NEW.match(new_line)

    if old_match and new_match:
        return Header(
            index_path=None,
            old_path=old_match.group(1),
            old_version=old_match.group(2) if old_match.group(2) else None,
            new_path=new_match.group(1),
            new_version=new_match.group(2) if new_match.group(2) else None,
        )
    return None
