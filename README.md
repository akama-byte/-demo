# stock-gem-bot

毎日自動で株式銘柄をスクリーニングし、Geminiで要約して通知するMVPです。

## 機能
- 銘柄データ取得: Yahoo Finance (`yfinance`)
- スクリーニング: 価格・時価総額・出来高倍率でスコアリング
- 要約: Gemini API (`google-genai`)
- 通知: Slack Webhook（未設定時は標準出力）
- 定期実行: `cron` で毎日実行

## セットアップ
```bash
cd /Users/tf-co0011/codex_folder/stock-gem-bot
./scripts/bootstrap.sh
cp .env.example .env
```

`.env` に必要な値を設定してください。
- `GEMINI_API_KEY`（未設定でも動作はしますが、LLM要約なし）
- `SLACK_WEBHOOK_URL`（未設定ならコンソール出力）

## 実行
```bash
source .venv/bin/activate
stock-gem-bot --dry-run
```

依存未導入でもローカル検証だけ行いたい場合:
```bash
PYTHONPATH=src python -m stock_gem_bot.cli --dry-run --mock
```

## 毎日自動実行（cron）
例: 平日 07:30 (JST) 実行
```bash
crontab -e
```
以下を追記:
```cron
30 7 * * 1-5 /Users/tf-co0011/codex_folder/stock-gem-bot/scripts/run_daily.sh >> /Users/tf-co0011/codex_folder/stock-gem-bot/logs/cron.log 2>&1
```

ログ先を使うなら先に作成:
```bash
mkdir -p /Users/tf-co0011/codex_folder/stock-gem-bot/logs
```

## 銘柄リスト差し替え
`config/symbols.txt` を編集し、Yahoo Financeのティッカー形式で記載してください。

## 注意
- 本アプリの出力は投資助言ではありません。
- 最終的な投資判断はご自身で行ってください。
