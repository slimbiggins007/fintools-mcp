# MCP Setup

Fintools runs as a local MCP server. Your assistant connects to the server and calls tools when it needs market context.

## Claude Code

```bash
claude mcp add fintools -- uvx --from fintools-mcp fintools-mcp
```

Restart Claude Code after registering the server.

## Claude Desktop

Edit the config file for your operating system:

- macOS: `~/Library/Application Support/Claude/claude_desktop_config.json`
- Windows: `%APPDATA%\Claude\claude_desktop_config.json`

Use:

```json
{
  "mcpServers": {
    "fintools": {
      "command": "uvx",
      "args": ["--from", "fintools-mcp", "fintools-mcp"]
    }
  }
}
```

Restart Claude Desktop after saving.

## Cursor

Create or edit Cursor's global MCP config:

- macOS/Linux: `~/.cursor/mcp.json`
- Windows: `%USERPROFILE%\.cursor\mcp.json`

Use the same local server configuration:

```json
{
  "mcpServers": {
    "fintools": {
      "command": "uvx",
      "args": ["--from", "fintools-mcp", "fintools-mcp"]
    }
  }
}
```

Restart Cursor after saving.

## Codex CLI

Register Fintools from a terminal:

```bash
codex mcp add fintools -- uvx --from fintools-mcp fintools-mcp
```

Or add the equivalent configuration to `~/.codex/config.toml`:

```toml
[mcp_servers.fintools]
command = "uvx"
args = ["--from", "fintools-mcp", "fintools-mcp"]
```

Start a new Codex session after registering the server.

## If The Client Cannot Find `uvx`

Some desktop apps inherit a smaller `PATH` than your terminal. Find the full
executable path:

```bash
which uvx
```

On Windows:

```text
where uvx
```

Replace `"command": "uvx"` with the full path returned by that command.

As an alternative, install the connector into a specific Python environment:

```bash
python -m pip install fintools-mcp
```

Then launch it through that same Python executable:

```json
{
  "mcpServers": {
    "fintools": {
      "command": "/full/path/to/python",
      "args": ["-m", "fintools_mcp"]
    }
  }
}
```

Use `which python` on macOS/Linux or `where python` on Windows to locate the
interpreter. On Windows, forward slashes or escaped backslashes are valid in
JSON paths.

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
