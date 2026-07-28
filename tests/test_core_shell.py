import asyncio
import json

from fintools_mcp import server
from fintools_mcp import data


def _loads(payload: str) -> dict:
    return json.loads(payload)


def test_about_fintools_describes_public_connector_and_paid_package():
    payload = _loads(server.about_fintools())

    assert payload["installed_package"] == "public Fintools connector"
    assert "get_stock_quote" in payload["public_connector_tools"]
    assert "get_trend_score" in payload["paid_fintools_mcp_tools"]
    assert payload["upgrade"]["status"] == "available"
    assert payload["upgrade"]["url"] == "https://whop.com/fintools/fintools-mcp/"


def test_check_connection():
    payload = _loads(server.check_connection())

    assert payload["status"] == "ok"
    assert payload["installed_package"] == "public Fintools connector"


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

    assert payload["installed_package"] == "public Fintools connector"
    assert payload["ticker"] == "SPY"
    assert payload["price"] == 100.0


def test_stock_quote_returns_clean_error_payload(monkeypatch):
    monkeypatch.setattr(
        server,
        "fetch_quote",
        lambda ticker: {
            "error": "no quote data for FAKE (unknown ticker or provider unavailable)",
            "ticker": ticker.upper(),
        },
    )

    payload = _loads(server.get_stock_quote("fake"))

    assert payload["ticker"] == "FAKE"
    assert payload["error"]
    assert payload["installed_package"] == "public Fintools connector"


def test_fetch_quote_returns_error_dict_on_provider_failure(monkeypatch):
    class ExplodingTicker:
        def __init__(self, symbol):
            self.symbol = symbol

        @property
        def fast_info(self):
            raise KeyError("exchangeTimezoneName")

    monkeypatch.setattr(data.yf, "Ticker", ExplodingTicker)

    quote = data.fetch_quote("faketickerxyz")

    assert quote["ticker"] == "FAKETICKERXYZ"
    assert "error" in quote


def test_paid_tools_return_upgrade_required():
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
        assert payload["required_package"] == "Fintools MCP"
        assert payload["upgrade"]["status"] == "available"
        assert payload["upgrade"]["discount_code"] == "FOUNDING"


def test_paid_stub_signatures_match_buyer_contract():
    tools = {tool.name: tool for tool in asyncio.run(server.mcp.list_tools())}
    market_snapshot_params = tools["get_market_snapshot"].inputSchema["properties"]
    winner_scan_params = tools["winner_similarity_scan"].inputSchema["properties"]

    assert set(market_snapshot_params) == {"ticker"}
    assert set(winner_scan_params) == {
        "tickers",
        "exclude_symbols",
        "max_results",
    }
    assert winner_scan_params["exclude_symbols"]["default"] == ""
    assert winner_scan_params["max_results"]["default"] == 20
