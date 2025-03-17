import asyncio
import logging

import typer
from typer import Typer

from Patche.app import logger
from Patche.mcp.server import serve

app = Typer()


@app.command()
# @app.option(
#     "--repository",
#     help="Repository to apply the patch",
#     default=None,
# )
# @app.option(
#     "--debug",
#     help="Enable debug mode",
#     default=False,
# )
def main(
    repository: str = typer.Option(
        None, "--repository", "-r", help="Repository to apply the patch"
    ),
    debug: bool = typer.Option(False, "--debug", "-d", help="Enable debug mode"),
):
    """
    Main entry point for the Patche MCP server.
    """

    logger.info("Starting Patche MCP server...")
    if debug:
        logger.setLevel(logging.DEBUG)

    asyncio.run(serve(repository))


if __name__ == "__main__":
    main()
