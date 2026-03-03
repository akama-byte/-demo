from __future__ import annotations


class SlackNotifier:
    def __init__(self, webhook_url: str | None) -> None:
        self.webhook_url = webhook_url

    def send(self, message: str) -> None:
        if not self.webhook_url:
            print(message)
            return

        try:
            import requests
        except Exception as exc:
            raise RuntimeError(
                "requests is not installed. Install project dependencies first."
            ) from exc

        response = requests.post(self.webhook_url, json={"text": message}, timeout=15)
        response.raise_for_status()
