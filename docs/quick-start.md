# Quick Start

This page gets the free Core connector running. Core is the public install path and the safest first test for any MCP client.

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

Core should call tools and return real tool output. If the assistant answers without calling tools, restart the MCP client and check the server registration.

## CLI Checks

```bash
fintools-mcp --version
fintools-mcp --about
```

## Next Step

Ask:

```text
What does Fintools Core include, and what requires Fintools Pro?
```

Core will explain the boundary. Advanced market-context work is handled by Fintools Pro.
