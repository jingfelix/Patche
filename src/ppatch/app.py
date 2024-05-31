import typer

from ppatch.utils.common import post_executed

app = typer.Typer(result_callback=post_executed)

from ppatch.commands.apply import apply
from ppatch.commands.auto import auto
from ppatch.commands.get import getpatches
from ppatch.commands.help import show_settings
from ppatch.commands.show import show
from ppatch.commands.trace import trace
