// Single source of truth for this server's tools. index.ts registers these
// with the MCP server, and export-tools.ts dumps the same array (minus
// handlers) to tools.json for mcp-stack-lint-schema and mcp-stack-eval-harness
// to read. Keep it this way, rather than hand-maintaining tools.json
// separately, so the lint/eval stages never drift from what the server
// actually serves.

export interface ToolDefinition {
  name: string;
  description: string;
  inputSchema: Record<string, unknown>;
  handler: (args: Record<string, unknown>) => Promise<{ content: Array<{ type: "text"; text: string }> }>;
}

export const tools: ToolDefinition[] = [
  {
    name: "__TOOL_NAME__",
    description:
      "__TOOL_DESCRIPTION__ Use this when <state the triggering situation>, not when <state the situation it should NOT be used for>.",
    inputSchema: {
      type: "object",
      properties: {
        input: {
          type: "string",
          description: "Replace with a real parameter: state its expected format/units so the calling model doesn't have to guess.",
        },
      },
      required: ["input"],
    },
    handler: async (args) => {
      const input = String(args.input ?? "");
      // Replace with the tool's real behavior. This must do something real -
      // a scaffold that throws "not implemented" fails mcp-stack-eval-harness
      // the moment it's run.
      return {
        content: [{ type: "text", text: `Received input: ${input}` }],
      };
    },
  },
];
