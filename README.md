# AutoTrading Lab

[![Python Checks](https://github.com/maduinos/AutoTrading/actions/workflows/python.yml/badge.svg)](https://github.com/maduinos/AutoTrading/actions/workflows/python.yml)

Personal cryptocurrency trading research scripts by Maduinos.

This repository is a hobby/lab project and is not part of the Maduinos FPGA business portfolio. It is kept public as an experiment archive and code-cleanup reference.

## Safety Notice

- This is not financial advice.
- Do not run live trading functions with real API keys unless you have reviewed the code and understand the risks.
- API keys must never be committed. Use environment variables or a local `ext_key` file copied from `ext_key.example`.
- Old exploratory scripts that mixed read-only API calls with live order calls were removed from the public tree.

## Requirements

- Python 3.10+
- Upbit account only if you intentionally run live trading functions
- TA-Lib native library if you use indicator calculations

Install Python packages:

```bash
python3 -m pip install -r requirements.txt
```

TA-Lib may require the native library first:

```bash
tar -xzf ta-lib-0.4.0-src.tar.gz
cd ta-lib/
./configure --prefix=/usr
make
sudo make install
```

## API Key Setup

Preferred:

```bash
export UPBIT_ACCESS_KEY="your-access-key"
export UPBIT_SECRET_KEY="your-secret-key"
```

Legacy local-file mode:

```bash
cp ext_key.example ext_key
chmod 600 ext_key
```

Then edit `ext_key` locally. The real `ext_key` file is ignored by Git.

## Scripts

| File | Purpose |
| --- | --- |
| `autotrading.py` | Trading helpers, TA-Lib indicator calculation, and an experimental RSI strategy loop |
| `data_history.py` | Downloads public candle history to CSV files |
| `get_mass_data.py` | Downloads larger OHLCV datasets through pyupbit |
| `tests/` | Import-safe smoke tests for helper behavior |

## Usage

Run tests:

```bash
python3 -m unittest discover -s tests -v
```

Download public candle CSV files:

```bash
python3 data_history.py --output-dir data --coins BTC ETH
```

Download a larger OHLCV file:

```bash
python3 get_mass_data.py --ticker KRW-XRP --interval m1 --batches 10 --output mass_data.csv
```

Run live strategy loop only after reviewing the source and setting API keys:

```bash
python3 autotrading.py
```

## License

MIT License. See `LICENSE`.

## Project Management

- Changes: `CHANGELOG.md`
- Release process: `RELEASE.md`
- Support scope: `SUPPORT.md`
- Contribution guide: `CONTRIBUTING.md`
- Security reporting: `SECURITY.md`
- Security history notes: `docs/security-history.md`
