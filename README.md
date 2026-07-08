# Fintools

[![PyPI version](https://img.shields.io/pypi/v/fintools-mcp.svg)](https://pypi.org/project/fintools-mcp/)
[![License: MIT](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)

Fintools gives AI assistants a local market-analysis toolbelt: computed quotes, trend context, technical levels, screens, options context, sizing math, candidate ranking, and repeatable playbooks.

The public package in this repository is a lightweight connector and documentation hub. It lets Claude, Codex, Cursor, or another MCP-compatible assistant prove that Fintools can run locally and fetch basic quote data. The full Fintools MCP package is a paid local download that contains the complete read-only market-analysis desk.

Fintools is not a broker, signal service, hedge fund, raw-data vendor, or investment adviser. It does not place trades. The point is simple: the AI writes around tool output instead of inventing market numbers.

## What Fintools MCP Includes

The paid Fintools MCP package includes the full local toolbelt:

| Area | Tools |
|---|---|
| Market / price context | `get_stock_quote`, `get_market_snapshot` |
| Technical analysis | `get_technical_indicators`, `get_trend_score`, `get_support_resistance` |
| Screening / ranking | `screen_stocks`, `find_breakouts`, `winner_similarity_scan`, `compare_tickers` |
| Options context | `analyze_options_chain`, `get_option_quote` |
| Risk / sizing | `calculate_position_size`, `calculate_atr_position` |
| Trade analytics | `analyze_trades` |
| Ops / data source | `get_data_source_stats` |

The buyer package also includes playbooks, sample reports, setup notes, guardrails, and report structure so the assistant gives useful market context with explicit caveats.

Get Fintools MCP:

```text
https://fintools.lemonsqueezy.com/checkout/buy/b14fb872-7073-4c53-b75f-2c04283da855
```

Founding code:

```text
FOUNDING
```

## Public Connector Quick Start

The public connector is useful for testing MCP wiring before buying or installing the full package.

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

If you ask the public connector for the full market-analysis toolbelt, it returns `upgrade_required` instead of pretending to compute something it does not include.

## Docs

| Page | What it covers |
|---|---|
| [Introduction](docs/introduction.md) | What Fintools is, what it is not, and why it exists |
| [Quick Start](docs/quick-start.md) | Install the public connector, connect an MCP client, and verify the setup |
| [Paid Package](docs/paid-package.md) | What ships in the paid Fintools MCP package |
| [Guardrails](docs/guardrails.md) | Read-only design, no trade recommendations, and "not checked" caveats |
| [MCP Setup](docs/mcp-setup.md) | Claude Code, Claude Desktop, Cursor-style MCP config, and reload checks |
| [Media Kit](docs/media-kit.md) | Screenshot and demo-clip checklist for GitHub, Lemon Squeezy, and launch posts |

## Guides

| Guide | What it shows |
|---|---|
| [Market Health Check](docs/guides/market-health-check.md) | Asking about broad market context without hallucinated numbers |
| [Candidate Scan](docs/guides/candidate-scan.md) | Finding and triaging names with Fintools MCP workflows |
| [Watchlist Review](docs/guides/watchlist-review.md) | Reviewing existing names and surfacing what changed |
| [Options Context](docs/guides/options-context.md) | Separating market setup from options-chain context |

## Broker Boundary

Fintools is broker-agnostic. Users can layer their own broker API, broker MCP, or account system into the same AI assistant workflow for live account data, positions, executable quotes, options-chain vetting, order routing, fills, and realized P&L. That broker layer is separate from Fintools.

Use Fintools for market context and research. Use your broker API/MCP or account system for broker truth and any execution workflow. Fintools itself remains read-only and does not place trades.

## Development

```bash
git clone https://github.com/slimbiggins007/fintools-mcp.git
cd fintools-mcp
uv sync
uv run python -m fintools_mcp
uv run pytest
```

## License

The public connector in this repository is MIT licensed. The paid Fintools MCP package is distributed separately.
