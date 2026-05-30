import argparse
import time

try:
    import pandas as pd
except ModuleNotFoundError:
    pd = None

try:
    import pyupbit
except ModuleNotFoundError:
    pyupbit = None


INTERVAL_ALIASES = {
    "m1": "minutes1",
    "m3": "minutes3",
    "m5": "minutes5",
    "m10": "minutes10",
    "m15": "minutes15",
    "m30": "minutes30",
    "m60": "minutes60",
    "m240": "minutes240",
    "d": "days",
    "w": "weeks",
    "month": "months",
}


def require_dependency(module, package_name):
    if module is None:
        raise RuntimeError(f"{package_name} is required. Install dependencies before downloading data.")
    return module


def resolve_interval(interval):
    try:
        return INTERVAL_ALIASES[interval]
    except KeyError as exc:
        supported = ", ".join(sorted(INTERVAL_ALIASES))
        raise ValueError(f"Unsupported interval '{interval}'. Supported values: {supported}") from exc


def download_mass_candles(ticker="KRW-XRP", interval="m1", batches=100, sleep_sec=0.5):
    require_dependency(pd, "pandas")
    require_dependency(pyupbit, "pyupbit")

    pyupbit_interval = resolve_interval(interval)
    df = pyupbit.get_ohlcv(ticker, interval=pyupbit_interval)
    if df is None:
        raise RuntimeError("Initial candle request returned no data.")

    df = df.reindex(index=df.index[::-1])
    remaining = batches
    while remaining > 0:
        df2 = pyupbit.get_ohlcv(ticker, interval=pyupbit_interval, to=df.index[-1])
        if df2 is None:
            time.sleep(sleep_sec)
            continue

        df2 = df2.reindex(index=df2.index[::-1])
        df = pd.concat([df, df2])
        remaining -= 1
        time.sleep(sleep_sec)

    df.reset_index(inplace=True)
    df.rename(columns={"index": "date"}, inplace=True)
    return df


def save_mass_data(df, output_path="mass_data.xlsx"):
    if output_path.endswith(".csv"):
        df.to_csv(output_path, index=False)
    else:
        df.to_excel(output_path, index=False)
    return output_path


def parse_args():
    parser = argparse.ArgumentParser(description="Download historical Upbit OHLCV data.")
    parser.add_argument("--ticker", default="KRW-XRP", help="Ticker such as KRW-XRP.")
    parser.add_argument("--interval", default="m1", help="Interval alias such as m1, m15, d, or w.")
    parser.add_argument("--batches", default=100, type=int, help="Number of older candle batches to request.")
    parser.add_argument("--output", default="mass_data.xlsx", help="Output .xlsx or .csv file.")
    return parser.parse_args()


def main():
    args = parse_args()
    started_at = time.time()
    df = download_mass_candles(args.ticker, args.interval, args.batches)
    save_mass_data(df, args.output)
    print("Saved:", args.output)
    print("Elapsed:", time.time() - started_at)


if __name__ == "__main__":
    main()
