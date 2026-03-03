from __future__ import annotations

import argparse

from .runner import run



def main() -> None:
    parser = argparse.ArgumentParser(description="Daily stock screener bot")
    parser.add_argument("--dry-run", action="store_true", help="Do not send notifications")
    parser.add_argument(
        "--mock",
        action="store_true",
        help="Use built-in mock market data for local testing",
    )
    args = parser.parse_args()

    print(run(dry_run=args.dry_run, use_mock=args.mock))


if __name__ == "__main__":
    main()
