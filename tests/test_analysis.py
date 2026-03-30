"""Tests for analysis tools."""

from fintools_mcp.analysis.trade_stats import compute_trade_stats
from fintools_mcp.analysis.position_sizer import calculate_position, atr_based_position


class TestTradeStats:
    def test_empty(self):
        stats = compute_trade_stats([])
        assert stats.total_trades == 0

    def test_basic_stats(self):
        pnls = [150, -80, 200, -50, 300, -120, 180, -40, 250, -90]
        stats = compute_trade_stats(pnls)
        assert stats.total_trades == 10
        assert stats.wins == 5
        assert stats.losses == 5
        assert stats.win_rate == 50.0
        assert stats.gross_pnl == 700.0
        assert stats.profit_factor > 1.0

    def test_all_winners(self):
        stats = compute_trade_stats([100, 200, 300])
        assert stats.win_rate == 100.0
        assert stats.max_consecutive_wins == 3

    def test_drawdown(self):
        pnls = [100, -500, -300, 200]
        stats = compute_trade_stats(pnls, starting_equity=10000)
        assert stats.max_drawdown > 0
        assert stats.max_drawdown_pct > 0


class TestPositionSizer:
    def test_basic_long(self):
        plan = calculate_position("AAPL", 180, 175, 195, 100000, 1.5)
        assert plan.direction == "long"
        assert plan.shares > 0
        assert plan.risk_reward_ratio == 3.0
        assert plan.total_risk <= 1500 + 5  # within 1.5% of 100k (+ rounding)

    def test_basic_short(self):
        plan = calculate_position("AAPL", 180, 185, 165, 100000, 1.5)
        assert plan.direction == "short"
        assert plan.shares > 0
        assert plan.risk_reward_ratio == 3.0

    def test_atr_position(self):
        plan = atr_based_position("SPY", 570, 8.0, 100000, 1.5, 2.0, 3.0, "long")
        assert plan.stop_price == 570 - 16  # 2x ATR
        assert plan.target_price == 570 + 24  # 3x ATR
        assert plan.shares > 0
