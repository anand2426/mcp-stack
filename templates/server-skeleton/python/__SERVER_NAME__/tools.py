"""
Single source of truth for this server's tools. server.py registers these
with the MCP server, and export_tools.py dumps the same TOOLS list (minus
handlers) to tools.json for mcp-stack-lint-schema and mcp-stack-eval-harness
to read. Keep it this way rather than hand-maintaining tools.json separately,
so the lint/eval stages never drift from what the server actually serves.
"""
from typing import Any, Awaitable, Callable, Dict, List

Handler = Callable[[Dict[str, Any]], Awaitable[str]]

TOOLS: List[Dict[str, Any]] = [
    {
        "name": "__TOOL_NAME__",
        "description": (
            "__TOOL_DESCRIPTION__ Use this when <state the triggering situation>, "
            "not when <state the situation it should NOT be used for>."
        ),
        "inputSchema": {
            "type": "object",
            "properties": {
                "input": {
                    "type": "string",
                    "description": "Replace with a real parameter: state its expected format/units "
                    "so the calling model doesn't have to guess.",
                }
            },
            "required": ["input"],
        },
    },
]


async def handle___TOOL_NAME__(args: Dict[str, Any]) -> str:
    input_value = str(args.get("input", ""))
    # Replace with the tool's real behavior. This must do something real -
    # a scaffold that returns a stub fails mcp-stack-eval-harness the moment
    # it's run.
    return f"Received input: {input_value}"


HANDLERS: Dict[str, Handler] = {
    "__TOOL_NAME__": handle___TOOL_NAME__,
}
