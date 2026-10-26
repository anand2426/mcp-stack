import asyncio

import mcp.server.stdio
import mcp.types as types
from mcp.server import Server
from mcp.server.models import InitializationOptions

from .tools import HANDLERS, TOOLS

server = Server("__SERVER_NAME__")


@server.list_tools()
async def list_tools() -> list[types.Tool]:
    return [
        types.Tool(name=t["name"], description=t["description"], inputSchema=t["inputSchema"])
        for t in TOOLS
    ]


@server.call_tool()
async def call_tool(name: str, arguments: dict) -> list[types.TextContent]:
    handler = HANDLERS.get(name)
    if handler is None:
        raise ValueError(f"Unknown tool: {name}")
    result_text = await handler(arguments or {})
    return [types.TextContent(type="text", text=result_text)]


async def _run() -> None:
    async with mcp.server.stdio.stdio_server() as (read_stream, write_stream):
        await server.run(
            read_stream,
            write_stream,
            InitializationOptions(
                server_name="__SERVER_NAME__",
                server_version="0.1.0",
                capabilities=server.get_capabilities(notification_options=None, experimental_capabilities={}),
            ),
        )


def main() -> None:
    asyncio.run(_run())


if __name__ == "__main__":
    main()
