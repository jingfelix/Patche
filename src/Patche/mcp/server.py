from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import Prompt, TextContent, Tool

from Patche.app import logger
from Patche.mcp.model import (
    PatcheApply,
    PatcheConfig,
    PatcheList,
    PatcheShow,
    PatcheTools,
)
from Patche.mcp.prompts import prompts
from Patche.mcp.tools import patche_apply, patche_config, patche_list, patche_show

server = None


async def serve(repository: str | None) -> None:

    if repository is None:
        logger.error("Repository is None")
        return

    server = Server(
        "patche-mcp",
        version="0.0.1",
        instructions="An MCP Server to show, list, apply or reverse patch to a file",
    )

    @server.list_tools()
    async def list_tools() -> list[Tool]:
        return [
            Tool(
                name=PatcheTools.CONFIG,
                description="Show the config of patche",
                inputSchema=PatcheConfig.model_json_schema(),
            ),
            Tool(
                name=PatcheTools.LIST,
                description="List all the patches in the directory",
                inputSchema=PatcheList.model_json_schema(),
            ),
            Tool(
                name=PatcheTools.SHOW,
                description="Show the patch",
                inputSchema=PatcheShow.model_json_schema(),
            ),
            Tool(
                name=PatcheTools.APPLY,
                description="Apply the patch",
                inputSchema=PatcheApply.model_json_schema(),
            ),
        ]

    @server.call_tool()
    async def call_tool(name: str, arguments: dict) -> list[TextContent]:
        """
        Call the tool with the given name and arguments.
        """

        logger.info(f"Received tool call: {name} with arguments: {arguments}")

        match name:
            case PatcheTools.CONFIG:
                config = patche_config()
                return [TextContent(type="text", text=f"Patche config: {config}")]
            case PatcheTools.LIST:
                patches = patche_list(arguments["patche_dir"])
                return [TextContent(type="text", text=f"Patche list: {patches}")]
            case PatcheTools.SHOW:
                patch = patche_show(arguments["patch_path"])
                return [TextContent(type="text", text=f"Patche show: {patch}")]
            case PatcheTools.APPLY:
                result = patche_apply(
                    arguments["patch_path"],
                    arguments["target_dir"],
                    arguments.get("reverse", False),
                )
                return [TextContent(type="text", text=f"Patche apply: {result}")]
            case _:
                raise NotImplementedError(f"Tool {name} is not implemented")

    @server.list_prompts()
    async def list_prompts() -> list[str]:
        """
        List all the prompts.
        """
        return prompts

    @server.call_prompt()
    async def call_prompt(name: str, arguments: dict) -> list[TextContent]:
        """
        Call the prompt with the given name and arguments.
        """
        logger.info(f"Received prompt call: {name} with arguments: {arguments}")
        raise NotImplementedError(f"Prompt {name} is not implemented")

    options = server.create_initialization_options()
    async with stdio_server() as (read_stream, write_stream):
        await server.run(read_stream, write_stream, options, raise_exceptions=True)
