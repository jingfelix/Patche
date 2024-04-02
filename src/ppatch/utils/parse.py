import datetime
import re
from collections import namedtuple

from whatthepatch import parse_patch as wtp_parse_patch

patchobj = namedtuple(
    "patchobj", ["sha", "author", "date", "subject", "message", "diff"]
)
git_diffcmd_header = re.compile("^diff --git a/(.+) b/(.+)$")
spliter_line = re.compile("^---$")


def parse_patch(text: str) -> patchobj:
    """
    Parse a patch file
    Diiference between this and whatthepatch.parse_patch is that this function also
    returns the sha, author, date and message of the commit
    """

    lines = text.splitlines()

    idx = 0
    for i, line in enumerate(lines):
        # 这里考虑 git log 格式和 git format-patch 格式
        if git_diffcmd_header.match(line) or spliter_line.match(line):
            idx = i
            break
    else:
        raise ValueError(
            "No diff --git line found, check if the input is a valid patch"
        )

    git_message_lines: list[str] = []
    if idx == 0:
        return patchobj(
            sha=None,
            author=None,
            date=None,
            subject=None,
            message=None,
            diff=wtp_parse_patch(text),
        )
    else:
        git_message_lines = lines[:idx]

    message = "\n".join(git_message_lines)

    sha_line = git_message_lines.pop(0)
    if sha_line.startswith("From ") or sha_line.startswith("commit "):
        sha = sha_line.split(" ")[1]
    else:
        sha = None

    author_line = git_message_lines.pop(0)
    if author_line.startswith("Author: ") or author_line.startswith("From:"):
        author = " ".join(author_line.split(" ")[1:])
    else:
        author = None

    date_line = git_message_lines.pop(0)
    if date_line.startswith("Date: "):
        date_str = date_line.split("Date: ")[1]
        # 解析 Thu, 7 Mar 2024 15:41:57 +0800 或 Tue Feb 2 16:07:37 2021 +0100
        if "," in date_str:
            date_fromat = "%a, %d %b %Y %H:%M:%S %z"
        else:
            date_fromat = "%a %b %d %H:%M:%S %Y %z"

        date = datetime.datetime.strptime(date_str.strip(), date_fromat)
    else:
        date = None

    # 如果接下来的一行以 Subject 开头，则直接解析出 subject
    if git_message_lines[0].startswith("Subject: "):
        subject = git_message_lines.pop(0).split("Subject: ")[1]
    else:
        # 否则找到剩余的行里第一个非换行/非空行作为 subject
        subject = None
        for line in git_message_lines:
            if line.strip() != "":
                subject = line
                break

    return patchobj(
        sha=sha.strip() if sha else None,
        author=author.strip() if author else None,
        date=date,
        subject=subject.strip() if subject else None,
        message=message,
        diff=wtp_parse_patch(text),
    )
