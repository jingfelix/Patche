import logging

import typer
from rich.logging import RichHandler

logging.basicConfig(level=logging.INFO, handlers=[RichHandler()], format="%(message)s")
logger = logging.getLogger()

from ppatch.utils.common import post_executed

app = typer.Typer(result_callback=post_executed)


@app.callback()
def callback(verbose: bool = False):
    """
    Entry for public options
    """
    if verbose:
        logger.setLevel(logging.DEBUG)


from ppatch.commands.apply import apply
from ppatch.commands.auto import auto
from ppatch.commands.get import getpatches
from ppatch.commands.help import show_settings
from ppatch.commands.show import show
from ppatch.commands.trace import trace
