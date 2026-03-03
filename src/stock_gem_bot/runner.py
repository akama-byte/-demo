from __future__ import annotations

from datetime import datetime
from zoneinfo import ZoneInfo

from .config import load_config
from .models import ScoredStock
from .notifier import SlackNotifier
from .providers import MockProvider, YahooFinanceProvider
from .screening import StockScreener
from .summarizer import GeminiSummarizer


def run_once(*, use_mock: bool = False) -> tuple[str, list[ScoredStock]]:
    cfg = load_config()
    provider = MockProvider() if use_mock else YahooFinanceProvider(cfg.symbols_file)
    screener = StockScreener(
        min_price=cfg.min_price,
        min_market_cap=cfg.min_market_cap,
        min_volume_ratio=cfg.min_volume_ratio,
        top_n=cfg.top_n,
    )
    summarizer = GeminiSummarizer(cfg.gemini_api_key, cfg.gemini_model)

    snapshots = provider.fetch()
    picks = screener.run(snapshots)

    now = datetime.now(tz=ZoneInfo(cfg.timezone)).strftime("%Y-%m-%d %H:%M %Z")
    summary = summarizer.summarize(picks)

    body = "\n".join([
        f"[Daily Stock Picks] {now}",
        "",
        summary,
        "",
        "注意: 本情報は投資助言ではありません。最終判断はご自身でお願いします。",
    ])
    return body, picks


def run(*, dry_run: bool = False, use_mock: bool = False) -> str:
    cfg = load_config()
    body, _ = run_once(use_mock=use_mock)

    if not dry_run:
        SlackNotifier(cfg.slack_webhook_url).send(body)

    return body
