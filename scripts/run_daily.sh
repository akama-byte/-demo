#!/usr/bin/env bash
set -euo pipefail

cd "$(dirname "$0")/.."
source .venv/bin/activate

if command -v stock-gem-bot >/dev/null 2>&1; then
  stock-gem-bot
else
  PYTHONPATH=src python -m stock_gem_bot.cli
fi
