"""Fintools Core — a limited MCP connector and Pro upgrade shell."""

from __future__ import annotations

import argparse
import json
from typing import Any

from mcp.server.fastmcp import FastMCP

from fintools_mcp import __version__
from fintools_mcp.data import fetch_quote, get_data_cache_stats

PUBLIC_PROJECT_URL = "https://github.com/slimbiggins007/fintools-mcp"
PRO_CHECKOUT_URL = "https://fintools.lemonsqueezy.com/checkout/buy/b14fb872-7073-4c53-b75f-2c04283da855"

CORE_TOOLS = [
    "about_fintools",
    "check_connection",
    "get_stock_quote",
    "get_data_source_stats",
]

PRO_TOOLS = [
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

PRO_CAPABILITIES = [
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
    "fintools-core",
    instructions=(
        "Fintools Core is the free MCP connector. It verifies that an AI assistant "
        "can connect to Fintools and fetch basic quote data. Trader workflow tools "
        "such as trend score, support/resistance, screening, options context, sizing, "
        "market snapshots, and candidate ranking require Fintools Pro and return "
        "upgrade_required in Core."
    ),
)


def _json(payload: dict[str, Any]) -> str:
    return json.dumps(payload, indent=2)


def _upgrade_required(tool_name: str, capability: str) -> str:
    return _json({
        "error": "upgrade_required",
        "tool": tool_name,
        "edition": "Fintools Core",
        "required_edition": "Fintools Pro",
        "message": f"{capability} is a Fintools Pro capability.",
        "core_includes": [
            "MCP connection check",
            "basic stock quote",
            "data/cache status",
            "product and license information",
        ],
        "pro_unlocks": PRO_CAPABILITIES,
        "upgrade": {
            "status": "available",
            "url": PRO_CHECKOUT_URL,
            "discount_code": "FOUNDING",
            "note": "Founding buyers can use FOUNDING while the first-25 discount is available.",
        },
        "boundaries": BOUNDARIES,
    })


@mcp.tool()
def about_fintools() -> str:
    """Explain Fintools Core vs Fintools Pro and route Pro-only requests honestly.

    Use this when a user asks what Fintools can do, what edition is installed,
    how to upgrade, or why a market-analysis workflow is unavailable in Core.
    """
    return _json({
        "product": "Fintools",
        "edition": "Core",
        "version": __version__,
        "summary": (
            "Fintools Core is the free MCP connector. It proves that the assistant "
            "can call Fintools locally and fetch basic market data. The trader "
            "workflow layer is Fintools Pro."
        ),
        "core_tools": CORE_TOOLS,
        "pro_tools": PRO_TOOLS,
        "pro_capabilities": PRO_CAPABILITIES,
        "upgrade": {
            "status": "available",
            "url": PRO_CHECKOUT_URL,
            "discount_code": "FOUNDING",
        },
        "public_project": PUBLIC_PROJECT_URL,
        "boundaries": BOUNDARIES,
    })


@mcp.tool()
def check_connection() -> str:
    """Confirm that the Fintools Core MCP server is connected and responding."""
    return _json({
        "status": "ok",
        "product": "Fintools",
        "edition": "Core",
        "version": __version__,
        "message": "Fintools Core MCP is connected.",
        "next_step": "Use get_stock_quote for a basic quote, or about_fintools for Core vs Pro details.",
    })


@mcp.tool()
def get_stock_quote(ticker: str) -> str:
    """Get a basic stock quote in Fintools Core.

    Args:
        ticker: Stock symbol, such as AAPL, SPY, or TSLA.
    """
    quote = fetch_quote(ticker)
    return _json({
        "edition": "Fintools Core",
        "ticker": quote.get("ticker", ticker.upper()),
        "price": quote.get("price"),
        "open": quote.get("open"),
        "high": quote.get("high"),
        "low": quote.get("low"),
        "previous_close": quote.get("previous_close"),
        "volume": quote.get("volume"),
        "market_cap": quote.get("market_cap"),
        "note": "Core provides basic quote data only. Trend, chart, options, sizing, scan, and desk workflows require Fintools Pro.",
    })


@mcp.tool()
def get_data_source_stats() -> str:
    """Show Fintools Core cache status and provider request counters."""
    stats = get_data_cache_stats()
    stats["edition"] = "Fintools Core"
    return _json(stats)


@mcp.tool()
def get_trend_score(ticker: str) -> str:
    """Fintools Pro required: graduated trend score with component breakdowns."""
    return _upgrade_required("get_trend_score", "Trend score")


@mcp.tool()
def get_technical_indicators(ticker: str, period: str = "3mo", interval: str = "1d") -> str:
    """Fintools Pro required: RSI, MACD, ATR, EMAs, Fibonacci, and chart context."""
    return _upgrade_required("get_technical_indicators", "Technical indicators and chart context")


@mcp.tool()
def get_support_resistance(ticker: str, lookback: int = 120, max_levels: int = 5) -> str:
    """Fintools Pro required: support/resistance levels and structure."""
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
    """Fintools Pro required: custom screens by trend, RSI, EMAs, and volume."""
    return _upgrade_required("screen_stocks", "Custom stock screening")


@mcp.tool()
def find_breakouts(
    exclude_symbols: str = "",
    min_trend_score: float = 30.0,
    min_rsi: float = 45.0,
    max_rsi: float = 75.0,
    max_results: int = 15,
) -> str:
    """Fintools Pro required: breakout discovery and candidate surfacing."""
    return _upgrade_required("find_breakouts", "Breakout discovery")


@mcp.tool()
def compare_tickers(tickers: list[str], period: str = "3mo") -> str:
    """Fintools Pro required: side-by-side technical comparison."""
    return _upgrade_required("compare_tickers", "Ticker comparison")


@mcp.tool()
def analyze_options_chain(
    ticker: str,
    expiration: str = "",
    min_volume: int = 10,
    min_open_interest: int = 100,
    max_spread_pct: float = 10.0,
) -> str:
    """Fintools Pro required: options-chain context and liquidity filters."""
    return _upgrade_required("analyze_options_chain", "Options-chain analysis")


@mcp.tool()
def get_option_quote(option_symbol: str, entry_price: float = 0.0) -> str:
    """Fintools Pro required: option quote, spread, IV, and entry P&L context."""
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
    """Fintools Pro required: risk-based position sizing."""
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
    """Fintools Pro required: ATR-based position sizing."""
    return _upgrade_required("calculate_atr_position", "ATR position sizing")


@mcp.tool()
def analyze_trades(pnls: list[float], starting_equity: float = 100000.0) -> str:
    """Fintools Pro required: trade-stat calculations and review context."""
    return _upgrade_required("analyze_trades", "Trade-stat analysis")


@mcp.tool()
def get_market_snapshot(ticker: str, period: str = "3mo") -> str:
    """Fintools Pro required: day-context gates, flags, and fresh_add_status."""
    return _upgrade_required("get_market_snapshot", "Market snapshot and day-context gates")


@mcp.tool()
def winner_similarity_scan(tickers: str, max_results: int = 25) -> str:
    """Fintools Pro required: winner-similarity candidate ranking and triage."""
    return _upgrade_required("winner_similarity_scan", "Winner-similarity candidate ranking")


def main() -> None:
    parser = argparse.ArgumentParser(description="Fintools Core MCP server")
    parser.add_argument("--version", action="store_true", help="print version and exit")
    parser.add_argument("--about", action="store_true", help="print Core vs Pro details and exit")
    args = parser.parse_args()

    if args.version:
        print(f"fintools-mcp {__version__} (Fintools Core)")
        return

    if args.about:
        print(about_fintools())
        return

    mcp.run(transport="stdio")


if __name__ == "__main__":
    main()
