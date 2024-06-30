import logging

import typer
from rich.console import Console
from rich.logging import RichHandler

logging.basicConfig(level=logging.INFO, handlers=[RichHandler()], format="%(message)s")
logger = logging.getLogger()

from ppatch.utils.common import post_executed

__version__ = "0.0.5b2"

app = typer.Typer(result_callback=post_executed, no_args_is_help=True)


@app.callback(invoke_without_command=True)
def callback(verbose: bool = False, version: bool = False):
    """
    Entry for public options
    """
    if verbose:
        logger.setLevel(logging.DEBUG)

    if version:
        console = Console()
        console.print(f"ppatch version {__version__}")
        raise typer.Exit()


from ppatch.commands.apply import apply
from ppatch.commands.auto import auto
from ppatch.commands.get import getpatches
from ppatch.commands.help import show_settings
from ppatch.commands.show import show
from ppatch.commands.symbol import getsymbol_command
from ppatch.commands.trace import trace
