"""Public Fintools connector and paid Fintools MCP routing shell."""

from __future__ import annotations

import argparse
import json
from typing import Any

from mcp.server.fastmcp import FastMCP

from fintools_mcp import __version__
from fintools_mcp.data import fetch_quote, get_data_cache_stats

PUBLIC_PROJECT_URL = "https://github.com/slimbiggins007/fintools-mcp"
PAID_CHECKOUT_URL = "https://whop.com/fintools/fintools-mcp/"

PUBLIC_TOOLS = [
    "about_fintools",
    "check_connection",
    "get_stock_quote",
    "get_data_source_stats",
]

PAID_TOOLS = [
    "get_trend_score",
    "get_technical_indicators",
    "get_support_resistance",
    "screen_stocks",
    "find_breakouts",
    "compare_tickers",
    "analyze_options_chain",
    "get_option_quote",
    "calculate_position_size",
    "calculate_atr_position",
    "analyze_trades",
    "get_market_snapshot",
    "winner_similarity_scan",
]

PAID_CAPABILITIES = [
    "trend scoring and component breakdowns",
    "technical indicators, support/resistance, and chart context",
    "stock screening, breakout discovery, and ticker comparison",
    "options-chain context and option quote analysis",
    "position sizing, ATR sizing, and trade statistics",
    "market snapshot day-context gates and fresh_add_status",
    "winner-similarity candidate ranking",
    "desk playbooks and report workflows",
]

BOUNDARIES = [
    "read-only market analysis software",
    "no broker execution",
    "no buy/sell/hold recommendations",
    "no investment advice",
    "no raw market data resale",
]

mcp = FastMCP(
    "fintools",
    instructions=(
        "This public Fintools connector verifies that an AI assistant can connect "
        "to Fintools and fetch basic quote data. Trader workflow tools "
        "such as trend score, support/resistance, screening, options context, sizing, "
        "market snapshots, and candidate ranking are included in the paid Fintools "
        "MCP package and return upgrade_required here."
    ),
)


def _json(payload: dict[str, Any]) -> str:
    return json.dumps(payload, indent=2)


def _upgrade_required(tool_name: str, capability: str) -> str:
    return _json({
        "error": "upgrade_required",
        "tool": tool_name,
        "installed_package": "public Fintools connector",
        "required_package": "Fintools MCP",
        "message": f"{capability} is included in the paid Fintools MCP package.",
        "public_connector_includes": [
            "MCP connection check",
            "basic stock quote",
            "data/cache status",
            "product and license information",
        ],
        "fintools_mcp_includes": PAID_CAPABILITIES,
        "upgrade": {
            "status": "available",
            "url": PAID_CHECKOUT_URL,
            "discount_code": "FOUNDING",
            "note": "Founding buyers can use FOUNDING while the first-25 discount is available.",
        },
        "boundaries": BOUNDARIES,
    })


@mcp.tool()
def about_fintools() -> str:
    """Explain the public connector and the paid Fintools MCP package.

    Use this when a user asks what Fintools can do, what package is installed,
    how to upgrade, or why a market-analysis workflow is unavailable here.
    """
    return _json({
        "product": "Fintools",
        "installed_package": "public Fintools connector",
        "version": __version__,
        "summary": (
            "This public connector proves that the assistant can call Fintools "
            "locally and fetch basic market data. The paid Fintools MCP package "
            "contains the market-analysis toolbelt and playbooks."
        ),
        "public_connector_tools": PUBLIC_TOOLS,
        "paid_fintools_mcp_tools": PAID_TOOLS,
        "paid_fintools_mcp_capabilities": PAID_CAPABILITIES,
        "upgrade": {
            "status": "available",
            "url": PAID_CHECKOUT_URL,
            "discount_code": "FOUNDING",
        },
        "public_project": PUBLIC_PROJECT_URL,
        "boundaries": BOUNDARIES,
    })


@mcp.tool()
def check_connection() -> str:
    """Confirm that the public Fintools connector is connected and responding."""
    return _json({
        "status": "ok",
        "product": "Fintools",
        "installed_package": "public Fintools connector",
        "version": __version__,
        "message": "Fintools public connector is connected.",
        "next_step": "Use get_stock_quote for a basic quote, or about_fintools for paid Fintools MCP details.",
    })


@mcp.tool()
def get_stock_quote(ticker: str) -> str:
    """Get a basic stock quote in the public Fintools connector.

    Args:
        ticker: Stock symbol, such as AAPL, SPY, or TSLA.
    """
    quote = fetch_quote(ticker)
    return _json({
        "installed_package": "public Fintools connector",
        "ticker": quote.get("ticker", ticker.upper()),
        "price": quote.get("price"),
        "open": quote.get("open"),
        "high": quote.get("high"),
        "low": quote.get("low"),
        "previous_close": quote.get("previous_close"),
        "volume": quote.get("volume"),
        "market_cap": quote.get("market_cap"),
        "note": "The public connector provides basic quote data only. Trend, chart, options, sizing, scan, and desk workflows are included in the paid Fintools MCP package.",
    })


@mcp.tool()
def get_data_source_stats() -> str:
    """Show public connector cache status and provider request counters."""
    stats = get_data_cache_stats()
    stats["installed_package"] = "public Fintools connector"
    return _json(stats)


@mcp.tool()
def get_trend_score(ticker: str) -> str:
    """Paid Fintools MCP required: graduated trend score with component breakdowns."""
    return _upgrade_required("get_trend_score", "Trend score")


@mcp.tool()
def get_technical_indicators(ticker: str, period: str = "3mo", interval: str = "1d") -> str:
    """Paid Fintools MCP required: RSI, MACD, ATR, EMAs, Fibonacci, and chart context."""
    return _upgrade_required("get_technical_indicators", "Technical indicators and chart context")


@mcp.tool()
def get_support_resistance(ticker: str, lookback: int = 120, max_levels: int = 5) -> str:
    """Paid Fintools MCP required: support/resistance levels and structure."""
    return _upgrade_required("get_support_resistance", "Support/resistance analysis")


@mcp.tool()
def screen_stocks(
    rsi_max: float | None = None,
    rsi_min: float | None = None,
    trend_min: float | None = None,
    trend_max: float | None = None,
    above_200ema: bool | None = None,
    above_50ema: bool | None = None,
    min_relative_volume: float | None = None,
    universe: str = "sp500",
    tickers: list[str] | None = None,
    max_results: int = 15,
) -> str:
    """Paid Fintools MCP required: custom screens by trend, RSI, EMAs, and volume."""
    return _upgrade_required("screen_stocks", "Custom stock screening")


@mcp.tool()
def find_breakouts(
    exclude_symbols: str = "",
    min_trend_score: float = 30.0,
    min_rsi: float = 45.0,
    max_rsi: float = 75.0,
    max_results: int = 15,
) -> str:
    """Paid Fintools MCP required: breakout discovery and candidate surfacing."""
    return _upgrade_required("find_breakouts", "Breakout discovery")


@mcp.tool()
def compare_tickers(tickers: list[str], period: str = "3mo") -> str:
    """Paid Fintools MCP required: side-by-side technical comparison."""
    return _upgrade_required("compare_tickers", "Ticker comparison")


@mcp.tool()
def analyze_options_chain(
    ticker: str,
    expiration: str = "",
    min_volume: int = 10,
    min_open_interest: int = 100,
    max_spread_pct: float = 10.0,
) -> str:
    """Paid Fintools MCP required: options-chain context and liquidity filters."""
    return _upgrade_required("analyze_options_chain", "Options-chain analysis")


@mcp.tool()
def get_option_quote(option_symbol: str, entry_price: float = 0.0) -> str:
    """Paid Fintools MCP required: option quote, spread, IV, and entry P&L context."""
    return _upgrade_required("get_option_quote", "Option quote analysis")


@mcp.tool()
def calculate_position_size(
    ticker: str,
    entry_price: float,
    stop_price: float,
    target_price: float,
    account_size: float = 100000.0,
    risk_pct: float = 1.5,
) -> str:
    """Paid Fintools MCP required: risk-based position sizing."""
    return _upgrade_required("calculate_position_size", "Position sizing")


@mcp.tool()
def calculate_atr_position(
    ticker: str,
    account_size: float = 100000.0,
    risk_pct: float = 1.5,
    stop_atr_mult: float = 2.0,
    target_atr_mult: float = 3.0,
    direction: str = "long",
    period: str = "3mo",
) -> str:
    """Paid Fintools MCP required: ATR-based position sizing."""
    return _upgrade_required("calculate_atr_position", "ATR position sizing")


@mcp.tool()
def analyze_trades(pnls: list[float], starting_equity: float = 100000.0) -> str:
    """Paid Fintools MCP required: trade-stat calculations and review context."""
    return _upgrade_required("analyze_trades", "Trade-stat analysis")


@mcp.tool()
def get_market_snapshot(ticker: str, period: str = "3mo") -> str:
    """Paid Fintools MCP required: day-context gates, flags, and fresh_add_status."""
    return _upgrade_required("get_market_snapshot", "Market snapshot and day-context gates")


@mcp.tool()
def winner_similarity_scan(tickers: str, max_results: int = 25) -> str:
    """Paid Fintools MCP required: winner-similarity candidate ranking and triage."""
    return _upgrade_required("winner_similarity_scan", "Winner-similarity candidate ranking")


def main() -> None:
    parser = argparse.ArgumentParser(description="Fintools public MCP connector")
    parser.add_argument("--version", action="store_true", help="print version and exit")
    parser.add_argument("--about", action="store_true", help="print Fintools package details and exit")
    args = parser.parse_args()

    if args.version:
        print(f"fintools-mcp {__version__} (public connector)")
        return

    if args.about:
        print(about_fintools())
        return

    mcp.run(transport="stdio")


if __name__ == "__main__":
    main()
