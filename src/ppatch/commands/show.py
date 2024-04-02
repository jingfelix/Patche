import os

import typer

from ppatch.app import app
from ppatch.utils.parse import parse_patch


@app.command()
def show(filename: str):
    """
    Show detail of a patch file.
    """
    if not os.path.exists(filename):
        typer.echo(f"Warning: {filename} not found!")
        return

    content = ""
    with open(filename, mode="r", encoding="utf-8") as (f):
        content = f.read()

    patch = parse_patch(content)

    typer.echo(f"Patch: {filename}")
    typer.echo(f"Sha: {patch.sha}")
    typer.echo(f"Author: {patch.author}")
    typer.echo(f"Date: {(patch.date).strftime('%Y-%m-%d %H:%M:%S')}")
    typer.echo(f"Subject: {patch.subject}")

    for diff in patch.diff:
        typer.echo(f"Diff: {diff.header.old_path} -> {diff.header.new_path}")
        # for i, change in enumerate(diff.changes):
        #     typer.echo(f"{i+1}: {change.hunk}")
