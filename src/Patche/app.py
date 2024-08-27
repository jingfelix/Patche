import logging

import typer
from rich.console import Console
from rich.logging import RichHandler

logging.basicConfig(level=logging.INFO, handlers=[RichHandler()], format="%(message)s")
logger = logging.getLogger()

from Patche.__version__ import __version__
from Patche.utils.common import post_executed

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
        console.print(f"patche version {__version__}")
        raise typer.Exit()


from Patche.commands.apply import apply
from Patche.commands.help import show_settings
from Patche.commands.show import show
