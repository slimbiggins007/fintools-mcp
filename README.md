# fintools-mcp

[![PyPI version](https://img.shields.io/pypi/v/fintools-mcp.svg)](https://pypi.org/project/fintools-mcp/)

Fintools Core is a free MCP connector that lets AI assistants verify a local Fintools setup, fetch basic stock quotes, and route advanced market-analysis requests honestly.

It is built for Claude, Codex, Cursor, and other MCP-compatible assistants. Core proves that the connection works and gives the assistant a clear boundary: basic quote/status tools are free; the market-context desk lives in Fintools Pro.

See [VISION.md](VISION.md) for the public product direction and guardrails.

## What Core Includes

| Tool | What it does |
|---|---|
| `about_fintools` | Explains what Core includes, what Pro includes, and where the boundary is |
| `check_connection` | Confirms the MCP server is connected |
| `get_stock_quote` | Fetches a basic stock quote |
| `get_data_source_stats` | Shows cache status and provider request counters |

Core is intentionally small. It is useful for verifying the install, checking that your assistant can call tools, and confirming basic market-data plumbing without an account or API key.

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

## Where Pro Begins

Fintools Pro is the paid local market-context desk. It contains the tools used for trader workflows: trend gates, day context, technical analysis, support/resistance, screens, breakout discovery, options context, sizing math, candidate ranking, and playbooks.

If you ask Core for a Pro workflow, Core returns `upgrade_required` instead of pretending to compute something it does not include.

For example:

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

That boundary is deliberate. Core proves the connector works. Pro is the market-context and research layer.

Fintools Pro is available at:

```text
https://fintools.lemonsqueezy.com/checkout/buy/b14fb872-7073-4c53-b75f-2c04283da855
```

Founding code: `FOUNDING`

## Core vs Pro

Fintools has two surfaces:

| Edition | What it is | Included |
|---|---|---|
| **Fintools Core** | Free connector/demo tier | MCP connection check, product info, basic stock quote, data/cache status |
| **Fintools Pro** | Paid local market-context desk | trend score, technical indicators, support/resistance, screens, breakout discovery, ticker comparison, options context, sizing math, market snapshot/day-context gates, winner-similarity ranking, playbooks |

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
