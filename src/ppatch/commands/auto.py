import os
import re
import subprocess

import typer

from ppatch.app import app
from ppatch.commands.get import getpatches
from ppatch.commands.trace import trace
from ppatch.config import settings
from ppatch.utils.common import process_title


@app.command()
def auto(filename: str):
    """Automatic do ANYTHING"""
    if not os.path.exists(filename):
        typer.echo(f"Warning: {filename} not found!")
        return

    # "patch -R -p1 -F 3 -i {filename}"
    # TODO: 令 apply patch 支持 -R -F 参数，将此处切换为自行实现的版本
    output: str = subprocess.run(
        ["patch", "-R", "-p1", "-F", "3", "-i", filename], capture_output=True
    ).stdout.decode("utf-8", errors="ignore")

    # 首先按照 patching file，将输出分割为几块
    output_parts: list[str] = []
    for line in output.splitlines():
        if line.startswith("patching file "):
            output_parts.append(line + "\n")
        else:
            output_parts[-1] += line + "\n"

    # 防呆设计
    # To do 添加 - n 交互
    output_parts = [part for part in output_parts if "Ignore -R" not in part]
    if len(output_parts) == 0:
        typer.echo("Unreversed patch detected!")
        raise typer.Exit()

    output_parts = [part for part in output_parts if "FAILED" in part]
    if len(output_parts) == 0:
        typer.echo("No failed patch")
        return

    # 确定每个 Part 里，有哪些文件，第几个 hunk 失败了
    fail_file_list: dict[str, list[int]] = {}
    for part in output_parts:
        file_name = part.splitlines()[0].split(" ")[-1]

        fail_hunk_list = []
        for line in part.splitlines():
            # 使用正则表达式匹配 hunk
            # Hunk #1 FAILED at 1.
            match = re.search(r"Hunk #(\d+) FAILED at (\d+).", line)
            if match:
                fail_hunk_list.append(int(match.group(1)))

        fail_file_list[file_name] = fail_hunk_list

    content = ""
    with open(filename, mode="r", encoding="utf-8") as (f):
        content = f.read()

    from ppatch.utils.parse import parse_patch

    subject = parse_patch(content).subject
    for file_name, hunk_list in fail_file_list.items():
        typer.echo(
            f"{len(hunk_list)} hunk(s) failed in {file_name} with subject {subject}"
        )

        sha_list = getpatches(file_name, subject, save=True)
        sha_for_sure = None

        for sha in sha_list:
            with open(
                os.path.join(
                    settings.base_dir,
                    settings.patch_store_dir,
                    f"{sha}-{process_title(file_name)}.patch",
                ),
                mode="r",
                encoding="utf-8",
            ) as (f):
                text = f.read()
                if parse_patch(text).subject == subject:
                    sha_for_sure = sha
                    break

        if sha_for_sure is None:
            typer.echo(f"Error: No patch found for {file_name}")
            return

        typer.echo(f"Found correspond patch {sha_for_sure} to {file_name}")
        typer.echo(f"Hunk list: {hunk_list}")

        for hunk in hunk_list:
            conflict_list = trace(file_name, from_commit=sha_for_sure, flag_hunk=hunk)
            typer.echo(f"Conflict list: {conflict_list}")
