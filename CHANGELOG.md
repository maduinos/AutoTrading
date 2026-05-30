# Changelog

## 2026-05-30

- Fixed ticker filtering in `search_dataframe()` and added regression coverage.
- Added a guarded `pyupbit` dependency check for current-price enrichment.
- Made candle-history collection respect explicit empty unit lists and report only files with downloaded rows.
- Removed tracked local key file and unsafe exploratory live-order examples.
- Added environment-variable based API key loading and a local `ext_key.example`.
- Made data collection scripts import-safe and testable.
- Added unit tests, CI, license, ignore rules, contribution guidance, and security policy.
