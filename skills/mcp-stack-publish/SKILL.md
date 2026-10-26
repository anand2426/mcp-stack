---
name: mcp-stack-publish
description: Version-bump, write a changelog entry, and prepare an MCP server for publishing to a registry - after the lint, security, and eval stages have passed. Use when the user is ready to ship their MCP server.
---

# mcp-stack-publish

The paperwork stage. This skill never runs on its own initiative — only when the user explicitly says they want to publish, and only after telling them which earlier stages have and haven't been run.

## Steps

1. Check whether `mcp-stack-lint-schema`, `mcp-stack-security-review`, and `mcp-stack-eval-harness` have been run against the current code in this session. If any haven't, say so explicitly and ask whether to run them first — do not publish on their behalf of an unreviewed server without the user overriding that explicitly.
2. Bump the version per semver: ask the user whether this is a patch/minor/major change if it's not obvious from the diff, and update it in `package.json`/`pyproject.toml` and the plugin/server manifest consistently.
3. Write a changelog entry (`CHANGELOG.md`) summarizing what changed, in the project's existing style if one exists.
4. Prepare the publish command for the target registry (npm, PyPI, or a Claude Code plugin marketplace's `marketplace.json` entry) but **do not run it**. Publishing is irreversible (a version can't be unpublished from most registries) and visible to others, so it falls under "explicit permission required" — show the exact command and diff, and wait for the user to say go.
5. After the user confirms and you run it, report the published URL/version and remind them `mcp-stack-canary` exists for ongoing monitoring.

## Hard rule

Never publish, push a tag, or create a GitHub release as a side effect of any other mcp-stack skill. This is the only skill allowed to do it, and only on explicit confirmation each time.
