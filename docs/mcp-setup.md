# MCP Setup

Fintools runs as a local MCP server. Your assistant connects to the server and calls tools when it needs market context.

## Claude Code

```bash
claude mcp add fintools -- uv run --from fintools-mcp fintools-mcp
```

Restart Claude Code after registering the server.

## Claude Desktop

Edit:

```text
~/Library/Application Support/Claude/claude_desktop_config.json
```

Use:

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

Restart Claude Desktop after saving.

## Verifying The Transport

Ask:

```text
Check the Fintools connection.
```

Then:

```text
Get a basic quote for SPY.
```

If the assistant does not call tools, the MCP client probably has not loaded the server.

## Reload Rule

MCP transports can be long-lived. If you change an MCP server path, package version, or local install, restart the client that owns the MCP process.

Do not debug a stale transport as if it were a market-data problem.

## Data Sources

The public connector uses free quote data and a local cache. It does not require account access or broker credentials.

Public connector cache defaults:

```bash
FINTOOLS_CACHE_ENABLED=0
FINTOOLS_CACHE_DIR=/path/to/cache
FINTOOLS_QUOTE_CACHE_TTL_SECONDS=15
```

Fintools MCP may use additional local configuration depending on the buyer's setup. It remains read-only.
