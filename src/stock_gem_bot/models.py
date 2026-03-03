from __future__ import annotations

from dataclasses import dataclass


@dataclass
class StockSnapshot:
    symbol: str
    price: float
    change_pct: float
    volume: int
    avg_volume: int
    market_cap: float


@dataclass
class ScoredStock:
    symbol: str
    score: float
    reason: str
    snapshot: StockSnapshot
