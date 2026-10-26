---
name: mcp-stack-eval-harness
description: Actually exercise an MCP server's tools with realistic calls and check the responses, instead of just checking that the code compiles. Use when the user wants to verify their MCP server works end-to-end before publishing.
---

# mcp-stack-eval-harness

A server that builds cleanly can still be broken in ways static checks never catch: wrong error handling, a tool that times out on real input, a schema that looks fine but the handler ignores half the fields. This skill runs it for real.

## Steps

1. Start the server locally (its own README/`mcp-stack-scaffold` output says how).
2. For each tool in `tools.json`, write 2-3 realistic test calls covering: a normal case, an edge case (empty/boundary input), and one deliberately malformed input to check error handling doesn't crash the server or leak a stack trace.
3. Drive these calls through an actual MCP client connection to the running server (not by calling the handler function directly in-process — the point is to catch protocol-level issues too: malformed JSON-RPC, wrong content types, missing required fields in responses).
4. For each call, check: did it return within a reasonable time, does the response shape match what the tool's schema promises, and does the result actually satisfy what the tool's description claims it does (read the description, then judge the output against it — this is the one check that catches "the schema lied").
5. Report a table: tool × test case × pass/fail × what went wrong. For failures, point at the specific line in the handler likely responsible.
6. Do not silently retry or paper over a flaky result — a tool that sometimes times out is a finding, not noise to average away.

## Boundary

This harness tests the server in isolation on synthetic calls. It is not a substitute for `mcp-stack-canary`'s job of watching the server after real traffic starts.
