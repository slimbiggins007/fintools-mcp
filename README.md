# fintools-mcp

Fintools Core is the free MCP connector for Fintools.

It verifies that Claude, Codex, Cursor, or another MCP-compatible assistant can connect to Fintools and fetch basic market data. The market-context workflow tools are paid Fintools Pro capabilities.

See [VISION.md](VISION.md) for the public product direction and guardrails.

## Core vs Pro

Fintools has two surfaces:

| Edition | What it is | Included |
|---|---|---|
| **Fintools Core** | Free connector/demo tier | MCP connection check, product info, basic stock quote, data/cache status |
| **Fintools Pro** | Paid local market-context desk | trend score, technical indicators, support/resistance, screens, breakout discovery, ticker comparison, options context, sizing math, market snapshot/day-context gates, winner-similarity ranking, playbooks |

Core is intentionally limited. If a user asks Core for a Pro workflow, the tool returns `upgrade_required` instead of pretending to compute something it does not include.

## Core Tools

| Tool | What it does |
|---|---|
| `about_fintools` | Explains Core vs Pro and routes Pro-only requests honestly |
| `check_connection` | Confirms the MCP server is connected |
| `get_stock_quote` | Fetches a basic stock quote |
| `get_data_source_stats` | Shows cache status and provider request counters |

## Pro-Gated Tools

These tool names are present in Core as hard paywall stubs. They return `upgrade_required` in Core and are implemented in Fintools Pro:

- `get_trend_score`
- `get_technical_indicators`
- `get_support_resistance`
- `screen_stocks`
- `find_breakouts`
- `compare_tickers`
- `analyze_options_chain`
- `get_option_quote`
- `calculate_position_size`
- `calculate_atr_position`
- `analyze_trades`
- `get_market_snapshot`
- `winner_similarity_scan`

## Quick Start

### Install

```bash
pip install fintools-mcp
```

Or with [uv](https://docs.astral.sh/uv/):

```bash
uv pip install fintools-mcp
```

### Add to Claude Desktop

Edit `~/Library/Application Support/Claude/claude_desktop_config.json`:

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

Or if installed via pip:

```json
{
  "mcpServers": {
    "fintools": {
      "command": "fintools-mcp"
    }
  }
}
```

### Add to Claude Code

```bash
claude mcp add fintools -- uv run --from fintools-mcp fintools-mcp
```

## CLI Checks

```bash
fintools-mcp --version
fintools-mcp --about
```

## Example Core Prompts

Once configured, ask:

- "Check the Fintools connection."
- "What does Fintools Core include?"
- "Get a basic quote for SPY."
- "Show Fintools data-source stats."

If you ask for trader workflow analysis:

```text
What's SPY's trend score?
```

Core returns:

```json
{
  "error": "upgrade_required",
  "required_edition": "Fintools Pro"
}
```

That boundary is deliberate. Core proves the connection works. Pro is the market-context and research layer.

## Data Sources

- **Basic stock quotes:** Yahoo Finance
- **Cache:** enabled by default at `~/.cache/fintools-mcp`
- No API keys are needed for Core.

Cache controls:

```bash
FINTOOLS_CACHE_ENABLED=0                 # disable cache
FINTOOLS_CACHE_DIR=/path/to/cache        # override cache location
FINTOOLS_QUOTE_CACHE_TTL_SECONDS=15      # default quote TTL
```

## Development

```bash
git clone https://github.com/slimbiggins007/fintools-mcp.git
cd fintools-mcp
uv sync
uv run python -m fintools_mcp  # starts the MCP server
```

Run tests:

```bash
uv run pytest
```

## Guardrails

Fintools is read-only market-analysis software. It is not a broker, signal service, hedge fund, raw-data vendor, or investment adviser. It does not place trades, route orders, manage funds, or provide buy/sell/hold recommendations.

## License

MIT
