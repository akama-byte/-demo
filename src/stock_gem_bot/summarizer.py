from __future__ import annotations

from collections.abc import Iterable

from .models import ScoredStock


class GeminiSummarizer:
    def __init__(self, api_key: str | None, model: str) -> None:
        self.api_key = api_key
        self.model = model

    def summarize(self, picks: Iterable[ScoredStock]) -> str:
        picks = list(picks)
        if not picks:
            return "本日の条件に一致する銘柄はありませんでした。"

        lines = [
            f"{idx}. {pick.symbol}: {pick.reason}"
            for idx, pick in enumerate(picks, start=1)
        ]
        structured = "\n".join(lines)

        if not self.api_key:
            return "\n".join([
                "GEMINI_API_KEY が未設定のため、ルールベース結果を返します。",
                structured,
            ])

        try:
            from google import genai
        except Exception:
            return "\n".join([
                "google-genai が未インストールのため、ルールベース結果を返します。",
                structured,
            ])

        client = genai.Client(api_key=self.api_key)
        prompt = (
            "あなたは日本株・米国株のマーケットアナリストです。"
            "次の候補銘柄を、過度な断定を避けて日本語で要約してください。"
            "形式: 銘柄ごとに1行、最後に全体のリスクを2行。\n\n"
            f"候補:\n{structured}"
        )

        response = client.models.generate_content(model=self.model, contents=prompt)
        return (response.text or "要約が空でした").strip()
