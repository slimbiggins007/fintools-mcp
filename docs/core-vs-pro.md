# Core vs Pro

Fintools is split into a free connector and a paid local market desk.

## Summary

| Edition | Purpose | Included |
|---|---|---|
| Fintools Core | Verify the MCP connection and fetch basic quote/status data | connection check, product info, basic quote, data/cache status |
| Fintools Pro | Run market-context and research workflows locally | trend gates, technical context, support/resistance, screens, breakout discovery, comparison, options context, sizing math, day context, candidate ranking, playbooks |

## Core

Core is free, public, local, and requires no API key.

Core tools:

| Tool | Purpose |
|---|---|
| `about_fintools` | Explain Core, Pro, and the upgrade boundary |
| `check_connection` | Confirm the MCP server is reachable |
| `get_stock_quote` | Fetch a basic stock quote |
| `get_data_source_stats` | Show cache/provider status |

Core is intentionally limited. It should not pretend to perform the paid market-context workflow.

## Pro

Pro is the paid local desk. It is built for traders who want AI assistants to answer market questions using computed tool output.

Pro capabilities include:

- trend score and trend-gate context
- technical indicators and chart context
- support/resistance
- breakout discovery
- custom screens
- ticker comparison
- options-chain context
- position sizing and ATR sizing
- market snapshots and day-context gates
- winner-similarity candidate ranking
- structured playbooks and report workflows

## Upgrade Boundary

If Core receives a Pro-shaped request, it returns `upgrade_required`.

Example:

```text
Run a winner similarity scan on AMD, CRWD, and SCHW.
```

Core does not approximate the result. It returns the paid boundary instead.

That is the product philosophy: computed numbers or an honest caveat, never invented analysis.

## Fintools Pro

```text
https://fintools.lemonsqueezy.com/checkout/buy/b14fb872-7073-4c53-b75f-2c04283da855
```

Founding code:

```text
FOUNDING
```
