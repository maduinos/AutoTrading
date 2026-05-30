# Contributing

This repository is a personal trading research lab, not business code and not financial advice.

## Scope

Good contributions include:

- Documentation improvements.
- Import-safe refactoring.
- Tests for helper functions.
- Safer handling of credentials, generated data, and local files.

Out of scope:

- Requests for financial advice or trading recommendations.
- Changes that require committed API keys or real account data.
- Live-order automation without clear risk documentation.

## Checklist

- Run `python3 -m unittest discover -s tests -v`.
- Run `python3 -m py_compile autotrading.py data_history.py get_mass_data.py tests/test_autotrading.py tests/test_data_history.py tests/test_get_mass_data.py`.
- Do not commit `ext_key`, `.env`, generated market data, or logs.

