# __SERVER_NAME__

An MCP server scaffolded by [mcp-stack](../../../README.md).

## What this does

<!-- Fill in: one paragraph on what this server lets an AI agent do. -->

## Setup

```bash
pip install -e .
```

## Register with Claude Code for local testing

```bash
claude mcp add __SERVER_NAME__ -- python -m __SERVER_NAME__.server
```

## Tools

Run `python -m __SERVER_NAME__.export_tools > tools.json` to regenerate `tools.json` from `tools.py` after changing any tool — `mcp-stack-lint-schema` and `mcp-stack-eval-harness` read that file.
