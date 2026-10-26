---
name: mcp-stack-canary
description: Periodically re-check a published MCP server to catch it silently breaking later - a dependency update, an upstream API change, an expired credential. Use when the user wants ongoing health monitoring for an already-published MCP server.
---

# mcp-stack-canary

A server that passed every check at publish time can still rot: the API it wraps changes its response shape, a dependency bump changes behavior, a test credential expires. This skill is the lightweight recurring check that catches that drift.

## Steps

1. Reuse the same test calls `mcp-stack-eval-harness` used at publish time (read them from `tools.json` / the eval report if saved) rather than inventing new ones — the point is to detect *change*, which needs a stable baseline.
2. Run them against the live/published server on a schedule the user sets (this plugin doesn't run itself — wire it up with the host's own scheduling, e.g. a cron job, GitHub Action, or Claude Code's own `/loop`/scheduled-task mechanism if available).
3. Compare each result against the last known-good response shape (not byte-for-byte — check the response still matches the tool's schema and the description's claim). Flag new error rates, new latency, or a changed response shape.
4. On a failure, report what changed and the most likely cause category (upstream API, dependency, expired credential, infra) rather than just "it broke" — point the user at where to look first.
5. Never attempt to auto-fix a canary failure (rotate a credential, roll back a dependency) — surface it and stop.

## Scope

This is a correctness/drift canary, not an uptime/latency SLO monitor — don't conflate it with production observability tooling if the server scales beyond a solo project.
