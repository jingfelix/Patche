import os
import subprocess

import typer
import whatthepatch

from ppatch.app import app
from ppatch.config import settings
from ppatch.model import ApplyResult, Diff, File, Line
from ppatch.utils.common import process_title, unpack
from ppatch.utils.resolve import apply_change


@app.command()
def trace(filename: str, from_commit: str = "", flag_hunk_list: list[int] = None):
    flag_hunk_list = [] if flag_hunk_list is None else flag_hunk_list

    if not os.path.exists(filename):
        typer.echo(f"Warning: {filename} not found!")
        return

    typer.echo(f"tracing patch {filename} from {from_commit}")

    output: str = subprocess.run(
        [
            "git",
            "log",
            "--pretty=format:%H",
            "--",
            filename,
        ],
        capture_output=True,
    ).stdout.decode("utf-8", errors="ignore")

    sha_list = output.splitlines()

    # 在 sha_list 中找到 from_commit 和 to_commit 的位置
    from_index = sha_list.index(from_commit) if from_commit else -1
    if from_index == -1:
        typer.echo(f"from_commit {from_commit} not found")
        return

    # 注意此处需要多选一个，包含 from commit 的前一个，用于 checkout
    sha_list = sha_list[: from_index + 2]

    typer.echo(f"Get {len(sha_list)} commits for {filename}")

    # checkout 到 from_commit 的前一个 commit
    subprocess.run(
        ["git", "checkout", sha_list.pop(), "--", filename],
        capture_output=True,
    )

    origin_file = File(file_path=filename)
    new_line_list = []
    # 首先将最后一个 patch 以 flag=True 的方式 apply
    from_commit_sha = sha_list.pop()
    assert from_commit_sha == from_commit
    typer.echo(f"Apply patch {from_commit_sha} to {filename}")
    patch_path = os.path.join(
        settings.base_dir,
        settings.patch_store_dir,
        f"{from_commit_sha}-{process_title(filename)}.patch",
    )

    for diff_ in whatthepatch.parse_patch(
        open(patch_path, mode="r", encoding="utf-8").read()
    ):
        diff = Diff(**unpack(diff_))
        if diff.header.old_path == filename or diff.header.new_path == filename:
            try:
                apply_result = apply_change(
                    diff.changes,
                    origin_file.line_list,
                    flag=True,
                    flag_hunk_list=flag_hunk_list,
                )
                # TODO: 检查失败数
                new_line_list = apply_result.new_line_list
            except Exception as e:
                typer.echo(f"Failed to apply patch {from_commit_sha}")
                typer.echo(f"Error: {e}")
                return
        else:
            typer.echo(f"Do not match with {filename}, skip")

    confict_list: dict[str, ApplyResult] = {}

    # 注意这里需要反向
    sha_list.reverse()
    for sha in sha_list:
        patch_path = os.path.join(
            settings.base_dir,
            settings.patch_store_dir,
            f"{sha}-{process_title(filename)}.patch",
        )

        apply_result: ApplyResult = ApplyResult()
        with open(patch_path, mode="r", encoding="utf-8") as (f):
            diffes = whatthepatch.parse_patch(f.read())

            for diff_ in diffes:
                diff = Diff(**unpack(diff_))
                if diff.header.old_path == filename or diff.header.new_path == filename:
                    try:
                        apply_result = apply_change(
                            diff.changes, new_line_list, trace=True, flag=True
                        )
                        new_line_list = apply_result.new_line_list

                        typer.echo(
                            f"Apply patch {sha} to {filename}: {len(new_line_list)}"
                        )
                    except Exception as e:
                        typer.echo(f"Failed to apply patch {sha}")
                        typer.echo(f"Error: {e}")

                        return
                else:
                    typer.echo(f"Do not match with {filename}, skip")

        if len(apply_result.conflict_hunk_num_list) > 0:
            confict_list[sha] = apply_result
            typer.echo(f"Conflict found in {sha}")
            typer.echo(f"Conflict hunk list: {apply_result.conflict_hunk_num_list}")

    # 写入文件
    with open(filename, mode="w+", encoding="utf-8") as (f):
        for line in new_line_list:
            if line.status:
                f.write(line.content + "\n")

    with open(filename + ".ppatch", mode="a+", encoding="utf-8") as (f):
        for line in new_line_list:
            if line.status:
                f.write(f"{line.index + 1}: {line.content} {line.flag}\n")

    typer.echo(f"Conflict count: {len(confict_list)}")

    return confict_list
