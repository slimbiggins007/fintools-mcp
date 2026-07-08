# Fintools

[![PyPI version](https://img.shields.io/pypi/v/fintools-mcp.svg)](https://pypi.org/project/fintools-mcp/)
[![License: MIT](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)

Fintools gives AI assistants a local MCP connector for market-analysis workflows.

Core is free, local, and requires no API key. It verifies that Claude, Codex, Cursor, or another MCP-compatible assistant can connect to Fintools, fetch basic quote data, and route advanced market-analysis requests honestly instead of inventing numbers.

Pro is the paid local market-context desk: trend gates, technical context, screens, breakout discovery, options context, sizing math, day-context flags, candidate ranking, and playbooks.

Fintools is read-only software. It is not a broker, signal service, hedge fund, raw-data vendor, or investment adviser.

## Docs

### Overview

| Page | What it covers |
|---|---|
| [Introduction](docs/introduction.md) | What Fintools is, what it is not, and why it exists |
| [Quick Start](docs/quick-start.md) | Install Core, connect an MCP client, and verify the setup |
| [Core vs Pro](docs/core-vs-pro.md) | The free connector boundary and the paid desk boundary |
| [Guardrails](docs/guardrails.md) | Read-only design, no trade recommendations, and "not checked" caveats |

### Integrations

| Page | What it covers |
|---|---|
| [MCP Setup](docs/mcp-setup.md) | Claude Code, Claude Desktop, Cursor-style MCP config, and reload checks |
| [Media Kit](docs/media-kit.md) | Screenshot and demo-clip checklist for GitHub, Lemon Squeezy, and launch posts |

### Guides

| Guide | What it shows |
|---|---|
| [Market Health Check](docs/guides/market-health-check.md) | Asking about broad market context without hallucinated numbers |
| [Candidate Scan](docs/guides/candidate-scan.md) | Finding and triaging names with Pro workflows |
| [Watchlist Review](docs/guides/watchlist-review.md) | Reviewing existing names and surfacing what changed |
| [Options Context](docs/guides/options-context.md) | Separating market setup from options-chain tradability context |

## Core Quick Start

Install the public Core connector:

```bash
pip install fintools-mcp
```

Add it to Claude Code:

```bash
claude mcp add fintools -- uv run --from fintools-mcp fintools-mcp
```

Ask:

```text
Check the Fintools connection.
```

Then ask:

```text
Get a basic quote for SPY.
```

Core includes:

| Tool | What it does |
|---|---|
| `about_fintools` | Explains Core, Pro, and the upgrade boundary |
| `check_connection` | Confirms the MCP server is connected |
| `get_stock_quote` | Fetches a basic stock quote |
| `get_data_source_stats` | Shows cache status and provider request counters |

## Where Pro Begins

If you ask Core for a Pro workflow, Core returns `upgrade_required` instead of pretending to compute something it does not include.

Example:

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

Fintools Pro:

```text
https://fintools.lemonsqueezy.com/checkout/buy/b14fb872-7073-4c53-b75f-2c04283da855
```

Founding code:

```text
FOUNDING
```

## Development

```bash
git clone https://github.com/slimbiggins007/fintools-mcp.git
cd fintools-mcp
uv sync
uv run python -m fintools_mcp
uv run pytest
```

## License

Fintools Core is MIT licensed. Fintools Pro is proprietary and distributed separately.
