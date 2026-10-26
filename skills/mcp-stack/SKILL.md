---
name: mcp-stack
description: Router for the mcp-stack plugin. Use when the user wants to build, lint, review, test, publish, or monitor an MCP server, or mentions "mcp-stack" by name.
---

# mcp-stack

`mcp-stack` is a pre-flight checklist for MCP (Model Context Protocol) servers. It exists because most MCP servers get published the same day they're written, with no one checking the tool descriptions make sense, the permissions aren't excessive, no secrets are committed, and the server actually works end-to-end with a real agent.

This skill is the router. Figure out which stage of the lifecycle the user is at and hand off to the matching skill:

| User's situation | Hand off to |
|---|---|
| Starting a brand-new MCP server from scratch | `mcp-stack-scaffold` |
| Has a server and wants its tool schemas checked for clarity/ambiguity | `mcp-stack-lint-schema` |
| Wants to check permissions, scopes, and for leaked secrets | `mcp-stack-security-review` |
| Wants to actually exercise the server with realistic calls before shipping | `mcp-stack-eval-harness` |
| Ready to version-bump, changelog, and publish | `mcp-stack-publish` |
| Already published, wants an ongoing health check | `mcp-stack-canary` |

If the user just says "run mcp-stack on this server" with no further detail, run the stages in order — scaffold is skipped if a server already exists, then lint-schema → security-review → eval-harness — and report a single consolidated checklist (pass/fail per stage) before asking whether to publish.

Never auto-publish, auto-commit, or auto-push as part of any stage. Every stage stops and reports findings; publishing always requires the user's explicit go-ahead (see `mcp-stack-publish`).
