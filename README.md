# mcp-stack

A pre-flight checklist and lifecycle toolkit for building and publishing [MCP](https://modelcontextprotocol.io) servers — the plugins that let an AI agent talk to a new tool (Gmail, a database, your own API).

**The problem:** MCP servers are easy to write and fast to publish, so most of them ship same-day with no one checking that the tool descriptions are clear, the permissions aren't overbroad, no secret got committed, and the server actually works end-to-end with a real agent. `mcp-stack` is the checklist that catches that before publishing — not after.

## What it is

A [Claude Code plugin](https://docs.claude.com/en/docs/claude-code/plugins) — install it and you get a set of skills covering the whole lifecycle of an MCP server:

| Stage | Skill | What it checks |
|---|---|---|
| Start | `mcp-stack-scaffold` | Generates a working server skeleton (TypeScript or Python) from a template, not a blank file. |
| Clarity | `mcp-stack-lint-schema` | Flags tool descriptions/parameters too vague or ambiguous for an agent to use correctly, no human in the loop to ask. |
| Safety | `mcp-stack-security-review` | Flags overbroad permissions, leaked secrets, and unsafe tool defaults (unguarded shell/write access). |
| Correctness | `mcp-stack-eval-harness` | Actually calls the server's tools through a real MCP connection and checks the responses match what's promised — not just that the code compiles. |
| Ship | `mcp-stack-publish` | Version bump, changelog, registry submission — only on your explicit go-ahead, never automatic. |
| Watch | `mcp-stack-canary` | Ongoing drift checks after publishing, so a later dependency/API change doesn't break it silently. |

Each stage can also hand off to a reviewer subagent (`agents/`) for a deeper pass: `schema-quality-reviewer`, `security-reviewer`, `dx-reviewer`.

## Install

```bash
# as a local plugin while developing it
claude --plugin-dir ./mcp-stack

# once published to a marketplace
/plugin install mcp-stack@<marketplace-name>
```

## Use

```
/mcp-stack
```

or just describe what you want ("lint my MCP server's tool schemas", "security-review this before I publish") and the router skill hands off to the right stage.

## Repo layout

```
mcp-stack/
  .claude-plugin/plugin.json   # plugin manifest
  skills/                      # one SKILL.md per lifecycle stage
  agents/                      # reviewer subagents invoked by the skills
  scripts/                     # standalone checkers the skills shell out to
  templates/server-skeleton/   # scaffold output for mcp-stack-scaffold
```

## Status

v0.1.0 — early. `lint_schema.py` and `secret_scan.py` are working standalone scripts; the rest of the lifecycle (eval harness, publish, canary) is currently agent-driven via the SKILL.md instructions rather than scripted. Contributions and real-world test reports welcome.

## License

MIT — see [LICENSE](LICENSE).
