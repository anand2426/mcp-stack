# __SERVER_NAME__

An MCP server scaffolded by [mcp-stack](../../../README.md).

## What this does

<!-- Fill in: one paragraph on what this server lets an AI agent do. -->

## Setup

```bash
npm install
npm run build
```

## Register with Claude Code for local testing

```bash
claude mcp add __SERVER_NAME__ -- node dist/index.js
```

## Tools

Run `npm run tools:export` to regenerate `tools.json` from `src/tools.ts` after changing any tool — `mcp-stack-lint-schema` and `mcp-stack-eval-harness` read that file.
