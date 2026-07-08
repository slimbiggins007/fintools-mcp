# Quick Start

This page gets the public Fintools connector running. It is the safest first test for any MCP client because it does not require account access, broker credentials, or the paid buyer package.

## Install

```bash
pip install fintools-mcp
```

Or with `uv`:

```bash
uv pip install fintools-mcp
```

## Claude Code

```bash
claude mcp add fintools -- uv run --from fintools-mcp fintools-mcp
```

Restart Claude Code after adding the MCP server.

## Claude Desktop

Edit:

```text
~/Library/Application Support/Claude/claude_desktop_config.json
```

Add:

```json
{
  "mcpServers": {
    "fintools": {
      "command": "uv",
      "args": ["run", "--from", "fintools-mcp", "fintools-mcp"]
    }
  }
}
```

Restart Claude Desktop after saving the config.

## Verify

Ask your assistant:

```text
Check the Fintools connection.
```

Then ask:

```text
Get a basic quote for SPY.
```

The public connector should call tools and return real tool output. If the assistant answers without calling tools, restart the MCP client and check the server registration.

## CLI Checks

```bash
fintools-mcp --version
fintools-mcp --about
```

## Full Fintools MCP

The complete market-analysis toolbelt is distributed as the paid Fintools MCP package:

```text
https://fintools.lemonsqueezy.com/checkout/buy/b14fb872-7073-4c53-b75f-2c04283da855
```
