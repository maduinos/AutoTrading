> 만든 사람: maduinos<br>
> 문서 만든 날짜: 2026-05-30<br>
> https://maduinos.blogspot.com/

# Contributing

This repository is a personal trading research lab, not business code and not financial advice.

## Scope

Good contributions include:

- Documentation improvements.
- Import-safe refactoring.
- Safer handling of credentials, generated data, and local files.

Out of scope:

- Requests for financial advice or trading recommendations.
- Changes that require committed API keys or real account data.
- Live-order automation without clear risk documentation.

## Checklist

- Run `python3 -m py_compile autotrading.py data_history.py get_mass_data.py`.
- Do not commit `ext_key`, `.env`, generated market data, or logs.
