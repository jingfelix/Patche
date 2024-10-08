import os
from typing import Annotated

import typer

from Patche.app import app, logger
from Patche.model import File
from Patche.utils.parse import parse_patch
from Patche.utils.resolve import apply_change


@app.command()
def apply(
    # filename: str,
    patch_path: str,
    reverse: Annotated[bool, typer.Option("-R", "--reverse")] = False,
    fuzz: Annotated[int, typer.Option("-F", "--fuzz")] = 0,
):
    """
    Apply a patch to a file.
    """

    if not os.path.exists(patch_path):
        logger.error(f"Warning: {patch_path} not found!")
        raise typer.Exit(code=1)

    if reverse:
        logger.info("Reversing patch...")

    has_failed = False

    with open(patch_path, mode="r", encoding="utf-8") as (f):
        diffes = parse_patch(f.read()).diff

        for diff in diffes:

            old_filename = diff.header.old_path
            new_filename = diff.header.new_path

            if os.path.exists(old_filename):

                logger.info(f"Applying patch to {old_filename}...")

                new_line_list = File(file_path=old_filename).line_list
                apply_result = apply_change(
                    diff.hunks, new_line_list, reverse=reverse, fuzz=fuzz
                )
                new_line_list = apply_result.new_line_list

                # 检查失败数
                for failed_hunk in apply_result.failed_hunk_list:
                    has_failed = True
                    logger.error(f"Failed hunk: {failed_hunk.index}")
            else:
                logger.error(f"{old_filename} not found!")
                raise typer.Exit(code=1)

            # 写入文件
            if not has_failed:
                with open(new_filename, mode="w+", encoding="utf-8") as f:
                    for line in new_line_list:
                        if line.status:
                            f.write(line.content + "\n")

    raise typer.Exit(code=1 if has_failed else 0)
