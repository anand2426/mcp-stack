#!/usr/bin/env python3
"""
mcp-stack schema linter.

Reads an MCP `tools/list`-shaped JSON file:
  { "tools": [ { "name": "...", "description": "...", "inputSchema": { ... } }, ... ] }

and flags the tool-schema mistakes that most commonly cause an AI agent to
misuse a tool: missing/vague descriptions, undocumented parameters,
oversized schemas, and duplicate tool names.

Usage:
  python lint_schema.py <path-to-tools.json> [--min-words N] [--max-schema-chars N]

Exit code: 0 if no findings, 1 if any findings (so it can gate CI).
"""
import argparse
import json
import sys

DEFAULT_MIN_WORDS = 10
DEFAULT_MAX_SCHEMA_CHARS = 4000


def word_count(text):
    return len(text.split()) if text else 0


def lint_tool(tool, min_words, max_schema_chars):
    findings = []
    name = tool.get("name", "<unnamed tool>")
    description = (tool.get("description") or "").strip()
    schema = tool.get("inputSchema") or {}

    if not description:
        findings.append((name, "error", "missing description",
                          "Add a description stating what this tool does AND when to call it."))
    elif word_count(description) < min_words:
        findings.append((name, "warn", "description too vague",
                          f"Only {word_count(description)} words. Expand to clarify when to use this "
                          f"tool vs. similarly named ones, e.g. 'Use when ... (not for ...)'."))

    schema_chars = len(json.dumps(schema))
    if schema_chars > max_schema_chars:
        findings.append((name, "warn", "schema may be too large",
                          f"inputSchema is {schema_chars} chars (threshold {max_schema_chars}). "
                          "Large schemas risk being skimmed or truncated by the calling model — "
                          "consider splitting this tool or simplifying the schema."))

    properties = schema.get("properties", {}) if isinstance(schema, dict) else {}
    required = set(schema.get("required", []) if isinstance(schema, dict) else [])
    for param_name, param_schema in properties.items():
        param_desc = (param_schema or {}).get("description", "").strip() if isinstance(param_schema, dict) else ""
        if not param_desc:
            severity = "error" if param_name in required else "warn"
            findings.append((name, severity, f"parameter '{param_name}' has no description",
                              f"Add a description for '{param_name}' — state its expected format/units "
                              "(e.g. ISO date, enum values) so the model doesn't have to guess."))

    return findings


def main():
    parser = argparse.ArgumentParser(description="Lint MCP tool schemas for agent-usability issues.")
    parser.add_argument("tools_json", help="Path to a tools/list-shaped JSON file")
    parser.add_argument("--min-words", type=int, default=DEFAULT_MIN_WORDS,
                         help=f"Minimum words in a description before it's flagged as vague (default {DEFAULT_MIN_WORDS})")
    parser.add_argument("--max-schema-chars", type=int, default=DEFAULT_MAX_SCHEMA_CHARS,
                         help=f"Max serialized inputSchema size before it's flagged (default {DEFAULT_MAX_SCHEMA_CHARS})")
    args = parser.parse_args()

    with open(args.tools_json, "r", encoding="utf-8") as f:
        data = json.load(f)

    tools = data.get("tools", [])
    if not tools:
        print("No tools found in input file.")
        sys.exit(0)

    all_findings = []
    seen_names = {}
    for tool in tools:
        name = tool.get("name", "<unnamed tool>")
        seen_names[name] = seen_names.get(name, 0) + 1
        all_findings.extend(lint_tool(tool, args.min_words, args.max_schema_chars))

    for name, count in seen_names.items():
        if count > 1:
            all_findings.append((name, "error", "duplicate tool name",
                                  f"'{name}' is defined {count} times — the model cannot reliably tell them apart."))

    if not all_findings:
        print(f"PASS — {len(tools)} tool(s) checked, no findings.")
        sys.exit(0)

    print(f"{len(all_findings)} finding(s) across {len(tools)} tool(s):\n")
    print(f"{'tool':<28} {'severity':<8} {'issue':<30} suggestion")
    print("-" * 100)
    errors = 0
    for name, severity, issue, suggestion in sorted(all_findings, key=lambda f: (f[1] != "error", f[0])):
        if severity == "error":
            errors += 1
        print(f"{name:<28} {severity:<8} {issue:<30} {suggestion}")

    print(f"\n{errors} error(s), {len(all_findings) - errors} warning(s).")
    sys.exit(1 if errors else 0)


if __name__ == "__main__":
    main()
