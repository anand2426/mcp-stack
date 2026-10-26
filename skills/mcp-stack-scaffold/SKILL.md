---
name: mcp-stack-scaffold
description: Generate a new MCP server skeleton (TypeScript or Python) with a correct manifest, one example tool, and a tools.json export the other mcp-stack skills can lint. Use when the user wants to start a brand-new MCP server.
---

# mcp-stack-scaffold

Generate a minimal, correct MCP server skeleton so the user starts from a working baseline instead of copy-pasting from a blog post.

## Steps

1. Ask (or infer from context) three things if not already given: server name (kebab-case), language (`typescript` or `python`), and the first tool it should expose (name + one-sentence purpose).
2. Copy the matching template from `templates/server-skeleton/<language>/` into the target directory, renaming placeholders (`__SERVER_NAME__`, `__TOOL_NAME__`, `__TOOL_DESCRIPTION__`).
3. Fill in the one example tool with a real `inputSchema` (JSON Schema) and a working handler — not a stub that throws "not implemented." A scaffold that doesn't run defeats the point.
4. Run the project's install command (`npm install` or `pip install -e .`) and its build/typecheck step. Fix any errors before handing back to the user — do not leave a scaffold that fails to build.
5. Write `tools.json` at the project root containing the `tools/list` shape:
   ```json
   { "tools": [ { "name": "...", "description": "...", "inputSchema": { ... } } ] }
   ```
   This is what `mcp-stack-lint-schema` and `mcp-stack-eval-harness` read, so keep it in sync whenever tools are added or changed — regenerate it from the server's actual tool definitions rather than hand-writing it, if the language/framework supports listing tools programmatically.
6. Add a `README.md` stub with: what the server does, how to run it locally, and the exact `claude mcp add` (or equivalent) command to register it for testing.
7. Tell the user what was created and suggest running `mcp-stack-lint-schema` next, once they've added their real tools.

## Non-goals

Do not scaffold authentication, rate limiting, or deployment config — those are server-specific decisions. Keep the skeleton to the minimum that runs.
