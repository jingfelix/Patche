import os

from rich.console import Console
from rich.table import Table

from ppatch.app import app, logger
from ppatch.utils.parse import parse_patch


@app.command()
def show(filename: str):
    """
    Show detail of a patch file.
    """
    if not os.path.exists(filename):
        logger.error(f"Warning: {filename} not found!")
        return

    content = ""
    with open(filename, mode="r", encoding="utf-8") as (f):
        content = f.read()

    patch = parse_patch(content)

    table = Table(box=None)
    table.add_column("Field", justify="left", style="cyan")
    table.add_column("Value", justify="left", style="magenta")

    table.add_row("Patch", filename)
    table.add_row("Sha", patch.sha)
    table.add_row("Author", patch.author)
    table.add_row("Date", (patch.date))
    table.add_row("Subject", patch.subject)

    for diff in patch.diff:
        table.add_row("Diff", f"{diff.header.old_path} -> {diff.header.new_path}")

    console = Console()
    console.print(table)
