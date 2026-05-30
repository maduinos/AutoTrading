import argparse
import csv
from pathlib import Path

import requests


DEFAULT_COINS = ["BTC", "ETH", "BSV", "XRP", "BCH", "EOS"]
DEFAULT_TIME_UNITS = ["days", "weeks"]
DEFAULT_MINUTE_UNITS = [1, 3, 5, 15, 30, 60, 240]


def build_candle_url(coin, unit):
    coin = coin.upper()
    if isinstance(unit, int) or str(unit).isdigit():
        return (
            "https://crix-api-endpoint.upbit.com/v1/crix/candles/"
            f"minutes/{unit}?code=CRIX.UPBIT.KRW-{coin}&count=400&"
        )
    return (
        "https://crix-api-endpoint.upbit.com/v1/crix/candles/"
        f"{unit}?code=CRIX.UPBIT.KRW-{coin}&count=100&"
    )


def normalize_candles(data):
    return [
        {
            "Time": candle["candleDateTimeKst"],
            "OpeningPrice": candle["openingPrice"],
            "HighPrice": candle["highPrice"],
            "LowPrice": candle["lowPrice"],
            "TradePrice": candle["tradePrice"],
            "CandleAccTradeVolume": candle["candleAccTradeVolume"],
            "CandleAccTradePrice": candle["candleAccTradePrice"],
        }
        for candle in data
    ]


def fetch_candles(coin, unit, timeout=10):
    response = requests.get(build_candle_url(coin, unit), timeout=timeout)
    response.raise_for_status()
    return normalize_candles(response.json())


def write_csv(rows, output_path):
    if not rows:
        return

    output_path.parent.mkdir(parents=True, exist_ok=True)
    with output_path.open("w", newline="", encoding="utf-8") as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def collect_history(coins=None, time_units=None, minute_units=None, output_dir="data"):
    coins = coins or DEFAULT_COINS
    time_units = time_units or DEFAULT_TIME_UNITS
    minute_units = minute_units or DEFAULT_MINUTE_UNITS
    output_dir = Path(output_dir)

    written_files = []
    for coin in coins:
        for unit in time_units:
            rows = fetch_candles(coin, unit)
            output_path = output_dir / f"{coin}_KRW_{unit}.csv"
            write_csv(rows, output_path)
            written_files.append(output_path)

        for unit in minute_units:
            rows = fetch_candles(coin, unit)
            output_path = output_dir / f"{coin}_KRW_{unit}.csv"
            write_csv(rows, output_path)
            written_files.append(output_path)

    return written_files


def parse_args():
    parser = argparse.ArgumentParser(description="Download public Upbit candle history as CSV files.")
    parser.add_argument("--output-dir", default="data", help="Directory for generated CSV files.")
    parser.add_argument("--coins", nargs="+", default=DEFAULT_COINS, help="Coin symbols without KRW- prefix.")
    return parser.parse_args()


def main():
    args = parse_args()
    files = collect_history(coins=args.coins, output_dir=args.output_dir)
    for file_path in files:
        print(file_path)


if __name__ == "__main__":
    main()
