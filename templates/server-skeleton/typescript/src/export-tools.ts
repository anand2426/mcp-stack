// Prints this server's tool list in `tools/list`-response shape, for
// mcp-stack's lint/eval skills to consume. Run via `npm run tools:export`.
import { tools } from "./tools.js";

const exported = {
  tools: tools.map(({ name, description, inputSchema }) => ({ name, description, inputSchema })),
};

console.log(JSON.stringify(exported, null, 2));
