"""Tests for technical indicators."""

from fintools_mcp.indicators.rsi import RSI, compute_rsi
from fintools_mcp.indicators.macd import MACD, compute_macd
from fintools_mcp.indicators.atr import ATR, compute_atr
from fintools_mcp.indicators.ema import EMA, compute_ema
from fintools_mcp.indicators.fibonacci import Fibonacci


def _sample_prices(n=60, base=100.0, trend=0.5, noise=2.0):
    """Generate sample price data."""
    closes = [base + i * trend + (i % 3 - 1) * noise for i in range(n)]
    highs = [c + 1.5 for c in closes]
    lows = [c - 1.5 for c in closes]
    return closes, highs, lows


class TestRSI:
    def test_needs_warmup(self):
        rsi = RSI(14)
        assert rsi.update(100.0) is None  # first bar, no prev close

    def test_returns_value_after_warmup(self):
        closes, _, _ = _sample_prices(30)
        result = compute_rsi(closes)
        assert result is not None
        assert 0 <= result <= 100

    def test_overbought_on_rising(self):
        closes = [100 + i for i in range(30)]  # straight up
        result = compute_rsi(closes)
        assert result > 70

    def test_oversold_on_falling(self):
        closes = [200 - i for i in range(30)]  # straight down
        result = compute_rsi(closes)
        assert result < 30


class TestMACD:
    def test_needs_warmup(self):
        macd = MACD()
        assert macd.update(100.0) is None

    def test_returns_result(self):
        closes, _, _ = _sample_prices(40)
        result = compute_macd(closes)
        assert result is not None
        assert hasattr(result, "macd_line")
        assert hasattr(result, "signal_line")
        assert hasattr(result, "histogram")

    def test_bullish_crossover(self):
        closes, _, _ = _sample_prices(60, trend=0.8)
        result = compute_macd(closes)
        assert result.macd_line > 0  # uptrend should have positive MACD


class TestATR:
    def test_needs_warmup(self):
        atr = ATR(14)
        assert atr.update(101, 99, 100) is None

    def test_returns_value(self):
        _, highs, lows = _sample_prices(30)
        closes = [(h + l) / 2 for h, l in zip(highs, lows)]
        result = compute_atr(highs, lows, closes)
        assert result is not None
        assert result > 0


class TestEMA:
    def test_needs_warmup(self):
        ema = EMA(20)
        assert ema.update(100.0) is None

    def test_returns_value(self):
        closes, _, _ = _sample_prices(30)
        result = compute_ema(closes, 20)
        assert result is not None

    def test_tracks_trend(self):
        closes = [100 + i for i in range(30)]
        result = compute_ema(closes, 10)
        assert result > closes[0]  # EMA should be above starting price in uptrend


class TestFibonacci:
    def test_needs_enough_bars(self):
        fib = Fibonacci(swing_lookback=50)
        result = fib.compute([100] * 10, [99] * 10, [100] * 10)
        assert result is None

    def test_returns_levels(self):
        closes, highs, lows = _sample_prices(60)
        fib = Fibonacci()
        result = fib.compute(highs, lows, closes)
        assert result is not None
        assert 0.618 in result.levels
        assert result.swing_high > result.swing_low
