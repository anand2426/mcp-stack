"""Prints this server's tool list in `tools/list`-response shape, for
mcp-stack's lint/eval skills to consume. Run via `python -m __SERVER_NAME__.export_tools`.
"""
import json

from .tools import TOOLS


def main() -> None:
    print(json.dumps({"tools": TOOLS}, indent=2))


if __name__ == "__main__":
    main()
