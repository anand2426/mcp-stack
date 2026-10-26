---
name: mcp-stack-lint-schema
description: Check an MCP server's tool definitions for the mistakes that make an AI agent misuse the tool - missing or vague descriptions, ambiguous parameter names, oversized schemas, duplicate tool names. Use when the user wants their MCP server's tool schemas reviewed before publishing.
---

# mcp-stack-lint-schema

The single biggest cause of an AI agent calling an MCP tool wrong is a badly written tool schema, not a bug in the server's code. This skill catches that before it ships.

## Steps

1. Get the server's tool definitions as a `tools/list`-shaped JSON file. If the user's project already has `tools.json` (written by `mcp-stack-scaffold`), use that. Otherwise, ask them to export it, or read the server's source and reconstruct the tool list yourself if it's small enough to do accurately — never guess at a schema you haven't actually seen.
2. Run the linter:
   ```bash
   python "${CLAUDE_PLUGIN_ROOT}/scripts/lint_schema.py" <path-to-tools.json>
   ```
3. The script reports, per tool: missing/empty `description`, descriptions under 10 words (too vague to disambiguate from similar tools), parameter names with no `description` field, schemas over the size threshold that risk being truncated or ignored by the model, and duplicate tool names across the file.
4. For every finding, don't just report the rule violation — rewrite the offending description/schema fragment as a concrete suggestion the user can paste in. "Description too vague" is useless without a drafted replacement.
5. Summarize as a pass/fail table (one row per tool) and ask whether to apply your suggested rewrites directly to the server's source, or just leave the report for the user to act on manually.

## What this does NOT check

This is a static lint, not a behavioral test — it can't tell you whether the tool's *handler* actually does what the description claims. That's `mcp-stack-eval-harness`'s job. Don't conflate the two when reporting results.
