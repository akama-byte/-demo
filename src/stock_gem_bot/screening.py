from __future__ import annotations

from .models import ScoredStock, StockSnapshot


class StockScreener:
    def __init__(
        self,
        *,
        min_price: float,
        min_market_cap: float,
        min_volume_ratio: float,
        top_n: int,
    ) -> None:
        self.min_price = min_price
        self.min_market_cap = min_market_cap
        self.min_volume_ratio = min_volume_ratio
        self.top_n = top_n

    def _score(self, snapshot: StockSnapshot) -> ScoredStock | None:
        if snapshot.price < self.min_price:
            return None
        if snapshot.market_cap < self.min_market_cap:
            return None
        if snapshot.avg_volume <= 0:
            return None

        volume_ratio = snapshot.volume / snapshot.avg_volume
        if volume_ratio < self.min_volume_ratio:
            return None

        score = (volume_ratio * 45.0) + (max(snapshot.change_pct, 0.0) * 7.0)
        reason = (
            f"出来高倍率 {volume_ratio:.2f}x, "
            f"前日比 {snapshot.change_pct:+.2f}%, "
            f"時価総額 {snapshot.market_cap / 1e9:.1f}B"
        )
        return ScoredStock(symbol=snapshot.symbol, score=score, reason=reason, snapshot=snapshot)

    def run(self, snapshots: list[StockSnapshot]) -> list[ScoredStock]:
        scored = [result for snapshot in snapshots if (result := self._score(snapshot)) is not None]
        return sorted(scored, key=lambda x: x.score, reverse=True)[: self.top_n]
