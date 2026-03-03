from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path


@dataclass
class AppConfig:
    symbols_file: Path
    top_n: int
    min_price: float
    min_market_cap: float
    min_volume_ratio: float
    gemini_api_key: str | None
    gemini_model: str
    slack_webhook_url: str | None
    timezone: str



def load_config() -> AppConfig:
    try:
        from dotenv import load_dotenv

        load_dotenv()
    except Exception:
        pass

    root = Path(__file__).resolve().parents[2]
    symbols_file = Path(os.getenv("SYMBOLS_FILE", root / "config" / "symbols.txt"))

    return AppConfig(
        symbols_file=symbols_file,
        top_n=int(os.getenv("TOP_N", "10")),
        min_price=float(os.getenv("MIN_PRICE", "200")),
        min_market_cap=float(os.getenv("MIN_MARKET_CAP", "20000000000")),
        min_volume_ratio=float(os.getenv("MIN_VOLUME_RATIO", "1.2")),
        gemini_api_key=os.getenv("GEMINI_API_KEY"),
        gemini_model=os.getenv("GEMINI_MODEL", "gemini-2.0-flash"),
        slack_webhook_url=os.getenv("SLACK_WEBHOOK_URL"),
        timezone=os.getenv("APP_TIMEZONE", "Asia/Tokyo"),
    )
