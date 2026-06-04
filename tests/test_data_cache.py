from __future__ import annotations

import pandas as pd

from fintools_mcp import data_cache
from fintools_mcp import data
from fintools_mcp.data import fetch_bars, fetch_bars_many


def _daily_frame(base: float = 100.0):
    index = pd.date_range("2026-01-01", periods=3, freq="D")
    return pd.DataFrame(
        {
            "Open": [base, base + 1, base + 2],
            "High": [base + 2, base + 3, base + 4],
            "Low": [base - 1, base, base + 1],
            "Close": [base + 1, base + 2, base + 3],
            "Volume": [1000, 1100, 1200],
        },
        index=index,
    )


def test_fetch_bars_uses_file_cache(monkeypatch, tmp_path):
    monkeypatch.setenv("FINTOOLS_CACHE_DIR", str(tmp_path))
    monkeypatch.delenv("FINTOOLS_DATA_SOURCE", raising=False)
    monkeypatch.setattr(data.public_bars, "is_enabled", lambda: False)
    data_cache.reset_stats()

    class FakeTicker:
        calls = 0

        def __init__(self, symbol):
            self.symbol = symbol

        def history(self, period, interval):
            FakeTicker.calls += 1
            return _daily_frame()

    monkeypatch.setattr(data.yf, "Ticker", FakeTicker)

    first = fetch_bars("AAPL", period="1y", interval="1d")
    second = fetch_bars("AAPL", period="1y", interval="1d")

    assert FakeTicker.calls == 1
    assert [bar.close for bar in second] == [bar.close for bar in first]
    stats = data_cache.stats()["counters"]
    assert stats["provider_yfinance_bars_requests"] == 1
    assert stats["hit"] >= 1


def test_fetch_bars_many_batches_uncached_symbols(monkeypatch, tmp_path):
    monkeypatch.setenv("FINTOOLS_CACHE_DIR", str(tmp_path))
    monkeypatch.delenv("FINTOOLS_DATA_SOURCE", raising=False)
    monkeypatch.setattr(data.public_bars, "is_enabled", lambda: False)
    data_cache.reset_stats()

    calls = {"download": 0}

    def fake_download(tickers, period, interval, group_by, auto_adjust, progress, threads):
        calls["download"] += 1
        symbols = tickers if isinstance(tickers, list) else [tickers]
        frames = []
        for i, symbol in enumerate(symbols):
            frame = _daily_frame(100 + i * 10)
            frame.columns = pd.MultiIndex.from_product([[symbol], frame.columns])
            frames.append(frame)
        return pd.concat(frames, axis=1)

    monkeypatch.setattr(data.yf, "download", fake_download)

    first = fetch_bars_many(["AAPL", "MSFT"], period="1y", interval="1d")
    second = fetch_bars_many(["AAPL", "MSFT"], period="1y", interval="1d")

    assert calls["download"] == 1
    assert set(first) == {"AAPL", "MSFT"}
    assert first["AAPL"][-1].close == 103.0
    assert second["MSFT"][-1].close == 113.0
    stats = data_cache.stats()["counters"]
    assert stats["provider_yfinance_batch_bars_requests"] == 1
    assert stats["hit"] >= 2
