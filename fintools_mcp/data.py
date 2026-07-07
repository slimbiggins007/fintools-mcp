"""Basic market quote fetching for Fintools Core."""

from __future__ import annotations

import math

import yfinance as yf

from fintools_mcp import data_cache


def _safe_number(value, default: float = 0.0):
    if value is None:
        return default
    try:
        if math.isnan(value):
            return default
    except TypeError:
        pass
    return value


def fetch_quote(ticker: str) -> dict:
    """Fetch a basic current quote summary for a ticker."""
    symbol = ticker.upper().strip()
    cache_key = data_cache.make_key("quote", "yfinance", symbol)
    cached = data_cache.get_json(cache_key, data_cache.ttl_seconds("quote"))
    if cached is not None:
        return cached

    tk = yf.Ticker(symbol)
    info = tk.fast_info
    data_cache.record_provider_request("yfinance", "quote")

    quote = {
        "ticker": symbol,
        "price": _safe_number(info.get("lastPrice")),
        "open": _safe_number(info.get("open")),
        "high": _safe_number(info.get("dayHigh")),
        "low": _safe_number(info.get("dayLow")),
        "previous_close": _safe_number(info.get("previousClose")),
        "volume": _safe_number(info.get("lastVolume"), 0),
        "market_cap": _safe_number(info.get("marketCap"), 0),
    }
    data_cache.set_json(cache_key, quote)
    return quote


def get_data_cache_stats() -> dict:
    """Return session cache counters and provider request counts."""
    return data_cache.stats()
