"""Public.com daily bars adapter for fintools-mcp.

Optional alternative to yfinance for daily bar data. Activated by setting
both FINTOOLS_DATA_SOURCE=public and PUBLIC_SECRET_KEY in the environment.
Falls back to yfinance silently on any failure.

Public's /historicdata/{SYMBOL}/{PERIOD} endpoint only supports DAILY bars at
period granularity (DAY, WEEK, MONTH, YEAR, FIVE_YEARS). Intraday intervals
(5m, 1h, etc) require Public's /marketdataservice/{SYM}/{PERIOD}/{INTERVAL}
endpoint which currently returns 403 (gated). For intraday, yfinance remains
the only path.
"""

from __future__ import annotations

import base64
import json as _json
import logging
import os
import re
import time
from datetime import datetime
from pathlib import Path

import httpx

_TICKER_RE = re.compile(r"^[A-Z0-9.\-]{1,10}$")

logger = logging.getLogger(__name__)


def _read_env_file_var(path: Path, key: str) -> str:
    """Extract `key=value` from a dotenv-style file. Empty string if absent."""
    if not path.is_file():
        return ""
    prefix = f"{key}="
    for line in path.read_text().splitlines():
        line = line.strip()
        if line.startswith(prefix):
            value = line.split("=", 1)[1]
            # Strip inline `#` comments (only when the # isn't inside quotes)
            if value and value[0] not in ("'", '"'):
                hash_idx = value.find("#")
                if hash_idx >= 0:
                    value = value[:hash_idx]
            return value.strip().strip('"').strip("'")
    return ""


def _from_env_or_files(key: str) -> str:
    """Resolve from process env, then ~/sre-v1/.env, then ~/fintools-mcp/.env."""
    val = os.getenv(key, "").strip()
    if val:
        return val
    for env_path in (Path.home() / "sre-v1" / ".env", Path.home() / "fintools-mcp" / ".env"):
        v = _read_env_file_var(env_path, key)
        if v:
            return v
    return ""


def _load_secret_key() -> str:
    return _from_env_or_files("PUBLIC_SECRET_KEY")


_BASE_URL = os.getenv("PUBLIC_BASE_URL", "https://api.public.com").rstrip("/")
_TOKEN_VALIDITY_MIN = 480
_REFRESH_BUFFER_SEC = 600

# yfinance period → (Public period, days to keep)
_PERIOD_MAP: dict[str, tuple[str, int]] = {
    "1d":   ("WEEK", 1),
    "5d":   ("WEEK", 5),
    "1mo":  ("MONTH", 22),
    "3mo":  ("YEAR", 66),
    "6mo":  ("YEAR", 126),
    "1y":   ("YEAR", 252),
    "2y":   ("FIVE_YEARS", 504),
    "5y":   ("FIVE_YEARS", 1260),
    "max":  ("FIVE_YEARS", 1260),
}


class _TokenCache:
    """Module-level JWT cache so all fetch_bars calls share one token."""
    token: str = ""
    expires_at: float = 0.0


def _ensure_token(secret_key: str) -> str:
    now = time.time()
    if _TokenCache.token and now < (_TokenCache.expires_at - _REFRESH_BUFFER_SEC):
        return _TokenCache.token

    with httpx.Client(timeout=10) as client:
        resp = client.post(
            f"{_BASE_URL}/userapiauthservice/personal/access-tokens",
            json={"secret": secret_key, "validityInMinutes": _TOKEN_VALIDITY_MIN},
        )
        resp.raise_for_status()
        _TokenCache.token = resp.json()["accessToken"]

    # Decode JWT exp claim
    try:
        parts = _TokenCache.token.split(".")
        payload = parts[1] + "=" * (-len(parts[1]) % 4)
        data = _json.loads(base64.urlsafe_b64decode(payload).decode())
        _TokenCache.expires_at = float(data.get("exp", now + _TOKEN_VALIDITY_MIN * 60))
    except Exception:
        _TokenCache.expires_at = now + _TOKEN_VALIDITY_MIN * 60

    return _TokenCache.token


def is_enabled() -> bool:
    """True if Public bars should be used for daily fetches.

    Resolved from process env or any of: ~/sre-v1/.env, ~/fintools-mcp/.env.
    Requires FINTOOLS_DATA_SOURCE=public AND a non-empty PUBLIC_SECRET_KEY.
    """
    if _from_env_or_files("FINTOOLS_DATA_SOURCE").lower() != "public":
        return False
    return bool(_load_secret_key())


def fetch_daily_bars(ticker: str, period: str = "6mo") -> list:
    """Fetch daily bars from Public. Returns list of fintools_mcp.data.Bar.

    Only daily bars supported. Caller must ensure interval='1d'.
    """
    from fintools_mcp.data import Bar  # local import to avoid circular

    secret = _load_secret_key()
    if not secret:
        raise RuntimeError("PUBLIC_SECRET_KEY not set")

    if not _TICKER_RE.match(ticker.upper()):
        raise ValueError(f"invalid ticker symbol: {ticker!r}")

    pub_period, days = _PERIOD_MAP.get(period, ("YEAR", 252))
    token = _ensure_token(secret)
    url = f"{_BASE_URL}/userapigateway/historicdata/{ticker.upper()}/{pub_period}"
    headers = {"Authorization": f"Bearer {token}", "Accept": "application/json"}

    with httpx.Client(timeout=15) as client:
        resp = client.get(url, headers=headers)
        resp.raise_for_status()
        data = resp.json()

    rm = data.get("regularMarket", {})
    raw_bars = rm.get("bars", []) if isinstance(rm, dict) else []
    bars: list = []
    for b in raw_bars:
        try:
            bars.append(Bar(
                timestamp=datetime.fromisoformat(b["timestamp"]),
                open=float(b["open"]),
                high=float(b["high"]),
                low=float(b["low"]),
                close=float(b["close"]),
                volume=float(b.get("volume", 0)),
            ))
        except (KeyError, ValueError):
            continue

    if len(bars) > days:
        bars = bars[-days:]
    return bars
