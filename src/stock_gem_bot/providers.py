from __future__ import annotations

from pathlib import Path

from .models import StockSnapshot


class YahooFinanceProvider:
    def __init__(self, symbols_file: Path) -> None:
        self.symbols_file = symbols_file

    def load_symbols(self) -> list[str]:
        symbols = [
            line.strip()
            for line in self.symbols_file.read_text(encoding="utf-8").splitlines()
            if line.strip() and not line.startswith("#")
        ]
        if not symbols:
            raise ValueError(f"No symbols found in {self.symbols_file}")
        return symbols

    def fetch(self) -> list[StockSnapshot]:
        try:
            import yfinance as yf
        except Exception as exc:
            raise RuntimeError(
                "yfinance is not installed. Install project dependencies first."
            ) from exc

        snapshots: list[StockSnapshot] = []
        for symbol in self.load_symbols():
            ticker = yf.Ticker(symbol)
            info = ticker.fast_info

            price = float(info.get("lastPrice") or 0.0)
            previous_close = float(info.get("previousClose") or 0.0)
            volume = int(info.get("lastVolume") or 0)
            avg_volume = int(info.get("tenDayAverageVolume") or info.get("threeMonthAverageVolume") or 0)
            market_cap = float(info.get("marketCap") or 0.0)

            if price <= 0 or previous_close <= 0:
                continue

            change_pct = ((price - previous_close) / previous_close) * 100

            snapshots.append(
                StockSnapshot(
                    symbol=symbol,
                    price=price,
                    change_pct=change_pct,
                    volume=volume,
                    avg_volume=avg_volume,
                    market_cap=market_cap,
                )
            )

        return snapshots


class MockProvider:
    def fetch(self) -> list[StockSnapshot]:
        return [
            StockSnapshot("AAPL", 195.2, 1.7, 78_000_000, 52_000_000, 2.9e12),
            StockSnapshot("NVDA", 892.0, 3.8, 61_000_000, 37_000_000, 2.2e12),
            StockSnapshot("TSLA", 182.4, -0.8, 120_000_000, 85_000_000, 5.8e11),
            StockSnapshot("PLTR", 25.6, 4.9, 98_000_000, 44_000_000, 5.2e10),
            StockSnapshot("AMD", 173.8, 2.1, 76_000_000, 39_000_000, 2.8e11),
        ]
