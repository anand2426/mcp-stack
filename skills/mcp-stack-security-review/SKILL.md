---
name: mcp-stack-security-review
description: Check an MCP server for overbroad permissions, committed secrets/API keys, and unsafe defaults before it is published. Use when the user wants a security pass on their MCP server.
---

# mcp-stack-security-review

Most MCP servers ask for more access than their tools actually use, and secret-scanning is skipped because there's no CI set up yet for a brand-new project. This skill is the gate that catches both before the server is public.

## Steps

1. **Secret scan.** Run:
   ```bash
   python "${CLAUDE_PLUGIN_ROOT}/scripts/secret_scan.py" <project-dir>
   ```
   This greps for common secret shapes (API key prefixes like `sk-`, `ghp_`, AWS key patterns, bare JWTs, `.env` files staged for commit) across tracked and untracked files. Treat any hit as blocking until the user confirms it's a placeholder/test value, not a real credential.
2. **Permission audit.** Read the server's declared scopes/permissions (OAuth scopes, filesystem paths it touches, env vars it reads, outbound hosts it calls) and cross-reference against what its tool handlers actually use. Flag anything requested but unused — e.g. a server that asks for `gmail.modify` but only ever reads messages should ask for `gmail.readonly`.
3. **Unsafe defaults.** Flag: tools that execute shell commands or arbitrary code with no allowlist, tools that write/delete without a dry-run or confirmation path, and any tool whose description doesn't match what broader access it silently requires.
4. Report findings ranked by severity (leaked real secret > overbroad permission > unsafe default > style nit). For each, state the concrete failure scenario it enables, not just the rule violated.
5. Never attempt to fix a leaked secret yourself (rotate keys, edit `.git` history) — that's irreversible and the user's call. State what leaked, where, and that it needs rotating and scrubbing from history before the repo goes public.

## Scope

This is a pre-publish gate for a small/solo project, not a substitute for a real third-party security audit before handling production user data at scale. Say so if the user's server does anything beyond that.
