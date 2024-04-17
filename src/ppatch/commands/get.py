import os
import re
import subprocess

import typer

from ppatch.app import app
from ppatch.config import settings
from ppatch.utils.common import process_title


@app.command("get")
def getpatches(filename: str, expression: str = None, save: bool = True) -> list[str]:
    """
    Get patches of a file.
    """
    if not os.path.exists(filename):
        typer.echo(f"Warning: {filename} not found!")
        return []

    typer.echo(f"Get patches of {filename}")

    output: str = subprocess.run(
        ["git", "log", "-p", "--", filename], capture_output=True
    ).stdout.decode("utf-8", errors="ignore")

    # 将 output 按照 commit ${hash}开头的行分割
    patches: list[str] = []
    for line in output.splitlines():
        if line.startswith("commit "):
            patches.append(line + "\n")
        else:
            patches[-1] += line + "\n"

    typer.echo(f"Get {len(patches)} patches for {filename}")

    pattern = re.compile(expression) if expression is not None else None

    sha_list = []
    for patch in patches:
        sha = patch.splitlines()[0].split(" ")[1]

        if pattern is not None and pattern.search(patch) is not None:
            sha_list.append(sha)
            typer.echo(f"Patch {sha} found with expression {expression}")

        patch_path = os.path.join(
            settings.base_dir,
            settings.patch_store_dir,
            f"{sha}-{process_title(filename)}.patch",
        )

        if save:
            if not os.path.exists(patch_path):
                with open(patch_path, mode="w+", encoding="utf-8") as (f):
                    f.write(patch)

    return sha_list
