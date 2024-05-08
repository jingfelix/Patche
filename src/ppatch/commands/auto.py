import os

import typer

from ppatch.app import app
from ppatch.commands.get import getpatches
from ppatch.commands.trace import trace
from ppatch.config import settings
from ppatch.model import Diff, File
from ppatch.utils.common import process_title, unpack
from ppatch.utils.parse import parse_patch
from ppatch.utils.resolve import apply_change


@app.command()
def auto(filename: str, output: str = typer.Option("", "--output", "-o")):
    """Automatic do ANYTHING"""
    if not os.path.exists(filename):
        typer.echo(f"Warning: {filename} not found!")
        return

    if not os.path.isdir(output):
        typer.echo(f"Warning: dir {output} not found!")
        return

    content = ""
    with open(filename, mode="r", encoding="utf-8") as (f):
        content = f.read()

    parser = parse_patch(content)
    fail_file_list: dict[str, list[int]] = {}
    raw_diffes = parser.diff  # TODO: patchobj 应该换成 Pydantic Model，然后注意换掉 unpack() 的调用
    for diff in raw_diffes:
        diff = Diff(**unpack(diff))
        target_file = diff.header.new_path  # 这里注意是 new_path 还是 old_path
        origin_file = File(file_path=target_file)

        apply_result = apply_change(
            diff.changes, origin_file.line_list, reverse=True, fuzz=3
        )

        if len(apply_result.failed_hunk_list) != 0:
            typer.echo(f"Failed hunk in {target_file}")
            fail_file_list[target_file] = [
                hunk.index for hunk in apply_result.failed_hunk_list
            ]

    if len(fail_file_list) == 0:
        typer.echo("No failed patch")
        return

    subject = parser.subject
    diffes: list = []
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

        conflict_list = trace(
            file_name, from_commit=sha_for_sure, flag_hunk_list=hunk_list
        )

        line_list = File(file_path=file_name).line_list
        conflict_list = list(conflict_list.items())
        conflict_list.reverse()

        for sha, apply_result in conflict_list:
            # 对 apply_result.failed_hunk_list 中的冲突块按照 hunk.index 进行排序
            apply_result.failed_hunk_list = sorted(
                apply_result.failed_hunk_list, key=lambda x: x.index
            )

            typer.echo(
                f"Conflict hunk in {sha}: {[hunk.index for hunk in apply_result.failed_hunk_list]}"
            )

            changes = []
            for hunk in apply_result.failed_hunk_list:
                changes.extend(hunk.all_)

            _apply_result = apply_change(changes, line_list, reverse=True)
            # TODO: 错误处理
            try:
                assert len(_apply_result.failed_hunk_list) == 0
            except AssertionError:
                typer.echo(
                    f"AUTO: Failed hunk in {sha}; len: {len(_apply_result.failed_hunk_list)}"
                )

            line_list = _apply_result.new_line_list

        origin_file = File(file_path=file_name)
        patched_text = "\n".join([line.content for line in line_list])
        origin_text = "\n".join([line.content for line in origin_file.line_list])

        import difflib

        diffes_ = difflib.unified_diff(
            origin_text.splitlines(),
            patched_text.splitlines(),
            fromfile="a/" + file_name,
            tofile="b/" + file_name,
        )

        for line in diffes_:
            diffes.append(line + "\n" if not line.endswith("\n") else line)

    with open(
        os.path.join(output, "auto.patch"),
        mode="w",
        encoding="utf-8",
    ) as (f):
        f.write("".join(diffes))
        typer.echo("Patch file generated: auto.patch")
