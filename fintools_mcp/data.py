"""Market data fetching.

Default source is yfinance. Optional Public.com bars source activated via
env vars FINTOOLS_DATA_SOURCE=public + PUBLIC_SECRET_KEY (or read from
~/.fintools/.env or ~/fintools-mcp/.env). Public is daily-only — intraday
intervals always use yfinance.
"""

from __future__ import annotations

import logging
from dataclasses import dataclass
from datetime import datetime
import math

import yfinance as yf

from fintools_mcp import data_cache
from fintools_mcp import public_bars

logger = logging.getLogger(__name__)


@dataclass
class Bar:
    timestamp: datetime
    open: float
    high: float
    low: float
    close: float
    volume: float


def fetch_bars(ticker: str, period: str = "1mo", interval: str = "1d") -> list[Bar]:
    """Fetch historical bars.

    Default source: yfinance. If FINTOOLS_DATA_SOURCE=public is set in the
    env AND PUBLIC_SECRET_KEY is available, daily bars (interval="1d") route
    through Public.com instead. Falls back to yfinance silently on Public
    failure. Intraday intervals always use yfinance.

    Args:
        ticker: Stock symbol (e.g. "AAPL")
        period: Data period — 1d, 5d, 1mo, 3mo, 6mo, 1y, 2y, 5y, max
        interval: Bar interval — 1m, 5m, 15m, 1h, 1d, 1wk, 1mo

    Returns:
        List of Bar objects, oldest first.
    """
    symbol = ticker.upper()
    source = "public" if interval == "1d" and public_bars.is_enabled() else "yfinance"
    cache_key = data_cache.make_key("bars", source, symbol, period, interval)
    cached = data_cache.get_json(cache_key, data_cache.ttl_seconds("bars", interval))
    if cached is not None:
        return [_bar_from_dict(row) for row in cached]

    if source == "public":
        try:
            bars = public_bars.fetch_daily_bars(symbol, period=period)
            data_cache.record_provider_request("public", "bars")
            data_cache.set_json(cache_key, data_cache.serialize_bars(bars))
            return bars
        except Exception as e:
            logger.warning(
                "Public bars failed for %s/%s — falling back to yfinance: %s",
                symbol, period, e,
            )
            source = "yfinance"
            cache_key = data_cache.make_key("bars", source, symbol, period, interval)
            cached = data_cache.get_json(cache_key, data_cache.ttl_seconds("bars", interval))
            if cached is not None:
                return [_bar_from_dict(row) for row in cached]

    tk = yf.Ticker(symbol)
    df = tk.history(period=period, interval=interval)
    data_cache.record_provider_request("yfinance", "bars")

    bars = _bars_from_dataframe(df)
    data_cache.set_json(cache_key, data_cache.serialize_bars(bars))
    return bars


def fetch_bars_many(
    tickers: list[str],
    period: str = "1mo",
    interval: str = "1d",
) -> dict[str, list[Bar]]:
    """Fetch bars for many tickers, using cache hits first and yfinance batching when possible."""
    symbols = _dedupe_symbols(tickers)
    results: dict[str, list[Bar]] = {}
    missing: list[str] = []
    source = "public" if interval == "1d" and public_bars.is_enabled() else "yfinance"
    ttl = data_cache.ttl_seconds("bars", interval)

    for symbol in symbols:
        cache_key = data_cache.make_key("bars", source, symbol, period, interval)
        cached = data_cache.get_json(cache_key, ttl)
        if cached is None:
            missing.append(symbol)
        else:
            results[symbol] = [_bar_from_dict(row) for row in cached]

    if not missing:
        return results

    if source == "public":
        for symbol in missing:
            results[symbol] = fetch_bars(symbol, period=period, interval=interval)
        return results

    try:
        df = yf.download(
            tickers=missing if len(missing) > 1 else missing[0],
            period=period,
            interval=interval,
            group_by="ticker",
            auto_adjust=False,
            progress=False,
            threads=True,
        )
        data_cache.record_provider_request("yfinance", "batch_bars")
        batched = _split_download_dataframe(df, missing)
        for symbol in missing:
            bars = batched.get(symbol, [])
            if not bars:
                bars = fetch_bars(symbol, period=period, interval=interval)
            results[symbol] = bars
            cache_key = data_cache.make_key("bars", "yfinance", symbol, period, interval)
            data_cache.set_json(cache_key, data_cache.serialize_bars(bars))
    except Exception as e:
        logger.warning("yfinance batch download failed for %s: %s", ",".join(missing), e)
        for symbol in missing:
            results[symbol] = fetch_bars(symbol, period=period, interval=interval)

    return results


def _bars_from_dataframe(df) -> list[Bar]:
    if df is None or df.empty:
        return []

    bars: list[Bar] = []
    for ts, row in df.iterrows():
        close = row.get("Close")
        if close is None or _is_nan(close):
            continue
        bars.append(Bar(
            timestamp=ts.to_pydatetime(),
            open=_safe_float(row.get("Open")),
            high=_safe_float(row.get("High")),
            low=_safe_float(row.get("Low")),
            close=_safe_float(close),
            volume=_safe_float(row.get("Volume")),
        ))
    return bars


def _split_download_dataframe(df, symbols: list[str]) -> dict[str, list[Bar]]:
    if df is None or df.empty:
        return {symbol: [] for symbol in symbols}

    if not hasattr(df.columns, "nlevels") or df.columns.nlevels == 1:
        return {symbols[0]: _bars_from_dataframe(df)} if len(symbols) == 1 else {}

    results: dict[str, list[Bar]] = {}
    level0 = set(str(v).upper() for v in df.columns.get_level_values(0))
    level1 = set(str(v).upper() for v in df.columns.get_level_values(1))
    for symbol in symbols:
        sub_df = None
        if symbol in level0:
            sub_df = df[symbol]
        elif symbol in level1:
            sub_df = df.xs(symbol, axis=1, level=1)
        results[symbol] = _bars_from_dataframe(sub_df) if sub_df is not None else []
    return results


def _bar_from_dict(row: dict) -> Bar:
    ts = row.get("timestamp")
    timestamp = datetime.fromisoformat(ts) if isinstance(ts, str) else ts
    return Bar(
        timestamp=timestamp,
        open=float(row.get("open", 0)),
        high=float(row.get("high", 0)),
        low=float(row.get("low", 0)),
        close=float(row.get("close", 0)),
        volume=float(row.get("volume", 0)),
    )


def _dedupe_symbols(tickers: list[str]) -> list[str]:
    seen: set[str] = set()
    out: list[str] = []
    for ticker in tickers:
        symbol = ticker.upper().strip()
        if symbol and symbol not in seen:
            seen.add(symbol)
            out.append(symbol)
    return out


def _safe_float(value, default: float = 0.0) -> float:
    if value is None or _is_nan(value):
        return default
    return float(value)


def _is_nan(value) -> bool:
    try:
        return math.isnan(value)
    except (TypeError, ValueError):
        return False


def fetch_options_chain(ticker: str, expiration: str | None = None) -> dict:
    """Fetch options chain from Yahoo Finance.

    Args:
        ticker: Stock symbol
        expiration: Expiration date (YYYY-MM-DD). If None, uses nearest expiration.

    Returns:
        Dict with 'calls', 'puts' (list of dicts), 'expirations' (list of date strings),
        and 'underlying_price'.
    """
    tk = yf.Ticker(ticker)
    data_cache.record_provider_request("yfinance", "options_chain")
    expirations = tk.options  # tuple of date strings

    if not expirations:
        return {"calls": [], "puts": [], "expirations": [], "underlying_price": 0}

    exp = expiration if expiration and expiration in expirations else expirations[0]
    chain = tk.option_chain(exp)

    underlying_price = tk.fast_info.get("lastPrice", 0) or 0

    def _safe_int(val, default=0):
        import math
        if val is None or (isinstance(val, float) and math.isnan(val)):
            return default
        return int(val)

    def _safe_float(val, default=0.0):
        import math
        if val is None or (isinstance(val, float) and math.isnan(val)):
            return default
        return float(val)

    def chain_to_dicts(df) -> list[dict]:
        records = []
        for _, row in df.iterrows():
            records.append({
                "contract": row.get("contractSymbol", ""),
                "strike": _safe_float(row.get("strike", 0)),
                "last": _safe_float(row.get("lastPrice", 0)),
                "bid": _safe_float(row.get("bid", 0)),
                "ask": _safe_float(row.get("ask", 0)),
                "volume": _safe_int(row.get("volume", 0)),
                "open_interest": _safe_int(row.get("openInterest", 0)),
                "iv": _safe_float(row.get("impliedVolatility", 0)),
                "in_the_money": bool(row.get("inTheMoney", False)),
            })
        return records

    return {
        "expiration": exp,
        "expirations": list(expirations),
        "underlying_price": underlying_price,
        "calls": chain_to_dicts(chain.calls),
        "puts": chain_to_dicts(chain.puts),
    }


def fetch_quote(ticker: str) -> dict:
    """Fetch current quote summary for a ticker."""
    symbol = ticker.upper()
    cache_key = data_cache.make_key("quote", "yfinance", symbol)
    cached = data_cache.get_json(cache_key, data_cache.ttl_seconds("quote"))
    if cached is not None:
        return cached

    tk = yf.Ticker(symbol)
    info = tk.fast_info
    data_cache.record_provider_request("yfinance", "quote")

    quote = {
        "ticker": symbol,
        "price": info.get("lastPrice", 0),
        "open": info.get("open", 0),
        "high": info.get("dayHigh", 0),
        "low": info.get("dayLow", 0),
        "previous_close": info.get("previousClose", 0),
        "volume": info.get("lastVolume", 0),
        "market_cap": info.get("marketCap", 0),
        "fifty_two_week_high": info.get("yearHigh", 0),
        "fifty_two_week_low": info.get("yearLow", 0),
    }
    data_cache.set_json(cache_key, quote)
    return quote


def get_data_cache_stats() -> dict:
    """Return session cache counters and provider request counts."""
    return data_cache.stats()
