"""Small file-backed cache for market data provider responses."""

from __future__ import annotations

import hashlib
import json
import os
import time
from collections import Counter
from dataclasses import asdict
from datetime import datetime
from pathlib import Path
from typing import Any


DEFAULT_CACHE_DIR = "~/.cache/fintools-mcp"

_stats: Counter[str] = Counter()


def is_enabled() -> bool:
    value = os.getenv("FINTOOLS_CACHE_ENABLED", "1").strip().lower()
    return value not in {"0", "false", "no", "off"}


def cache_dir() -> Path:
    return Path(os.getenv("FINTOOLS_CACHE_DIR", DEFAULT_CACHE_DIR)).expanduser()


def ttl_seconds(kind: str, interval: str = "") -> int:
    if kind == "quote":
        return int(os.getenv("FINTOOLS_QUOTE_CACHE_TTL_SECONDS", "15"))
    if interval in {"1m", "2m", "5m", "15m", "30m", "60m", "90m", "1h"}:
        return int(os.getenv("FINTOOLS_INTRADAY_CACHE_TTL_SECONDS", "60"))
    if interval == "1d":
        return int(os.getenv("FINTOOLS_DAILY_CACHE_TTL_SECONDS", "900"))
    return int(os.getenv("FINTOOLS_CACHE_TTL_SECONDS", "3600"))


def make_key(*parts: object) -> str:
    raw = json.dumps([str(p) for p in parts], separators=(",", ":"), sort_keys=True)
    return hashlib.sha256(raw.encode("utf-8")).hexdigest()


def _path(key: str) -> Path:
    return cache_dir() / f"{key}.json"


def get_json(key: str, ttl: int) -> Any | None:
    if not is_enabled():
        _stats["disabled"] += 1
        return None

    path = _path(key)
    try:
        payload = json.loads(path.read_text())
    except FileNotFoundError:
        _stats["miss"] += 1
        return None
    except Exception:
        _stats["read_error"] += 1
        return None

    created_at = float(payload.get("created_at") or 0)
    if time.time() - created_at > ttl:
        _stats["stale"] += 1
        return None

    _stats["hit"] += 1
    return payload.get("data")


def set_json(key: str, data: Any) -> None:
    if not is_enabled():
        return

    directory = cache_dir()
    try:
        directory.mkdir(parents=True, exist_ok=True)
        path = _path(key)
        tmp = path.with_suffix(".tmp")
        tmp.write_text(json.dumps({"created_at": time.time(), "data": data}, separators=(",", ":")))
        tmp.replace(path)
        _stats["write"] += 1
    except Exception:
        _stats["write_error"] += 1


def serialize_bars(bars: list[Any]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for bar in bars:
        row = asdict(bar)
        ts = row.get("timestamp")
        if isinstance(ts, datetime):
            row["timestamp"] = ts.isoformat()
        rows.append(row)
    return rows


def record_provider_request(provider: str, kind: str, count: int = 1) -> None:
    _stats[f"provider_{provider}_{kind}_requests"] += count


def stats() -> dict[str, Any]:
    return {
        "enabled": is_enabled(),
        "cache_dir": str(cache_dir()),
        "counters": dict(_stats),
    }


def reset_stats() -> None:
    _stats.clear()
