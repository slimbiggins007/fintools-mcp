import json

from fintools_mcp import server


def _loads(payload: str) -> dict:
    return json.loads(payload)


def test_about_fintools_describes_core_and_pro():
    payload = _loads(server.about_fintools())

    assert payload["edition"] == "Core"
    assert "get_stock_quote" in payload["core_tools"]
    assert "get_trend_score" in payload["pro_tools"]
    assert payload["upgrade"]["status"] == "available"
    assert payload["upgrade"]["url"].startswith("https://fintools.lemonsqueezy.com/checkout/")


def test_check_connection():
    payload = _loads(server.check_connection())

    assert payload["status"] == "ok"
    assert payload["edition"] == "Core"


def test_stock_quote_uses_basic_quote(monkeypatch):
    monkeypatch.setattr(
        server,
        "fetch_quote",
        lambda ticker: {
            "ticker": ticker.upper(),
            "price": 100.0,
            "open": 99.0,
            "high": 101.0,
            "low": 98.5,
            "previous_close": 99.5,
            "volume": 12345,
            "market_cap": 1000000,
        },
    )

    payload = _loads(server.get_stock_quote("spy"))

    assert payload["edition"] == "Fintools Core"
    assert payload["ticker"] == "SPY"
    assert payload["price"] == 100.0


def test_pro_tools_return_upgrade_required():
    checks = [
        server.get_trend_score("SPY"),
        server.get_technical_indicators("SPY"),
        server.get_support_resistance("SPY"),
        server.screen_stocks(),
        server.find_breakouts(),
        server.compare_tickers(["SPY", "QQQ"]),
        server.analyze_options_chain("SPY"),
        server.get_option_quote("SPY260117C00500000"),
        server.calculate_position_size("SPY", 100, 95, 110),
        server.calculate_atr_position("SPY"),
        server.analyze_trades([1, -1]),
        server.get_market_snapshot("SPY"),
        server.winner_similarity_scan("SPY,QQQ"),
    ]

    for raw in checks:
        payload = _loads(raw)
        assert payload["error"] == "upgrade_required"
        assert payload["required_edition"] == "Fintools Pro"
        assert payload["upgrade"]["status"] == "available"
        assert payload["upgrade"]["discount_code"] == "FOUNDING"
