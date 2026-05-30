import unittest
from pathlib import Path
import tempfile
from unittest.mock import patch

import data_history


class DataHistoryTest(unittest.TestCase):
    def test_build_candle_url_for_day_unit(self):
        url = data_history.build_candle_url("BTC", "days")

        self.assertEqual(
            url,
            "https://crix-api-endpoint.upbit.com/v1/crix/candles/days?code=CRIX.UPBIT.KRW-BTC&count=100&",
        )

    def test_build_candle_url_for_minute_unit(self):
        url = data_history.build_candle_url("ETH", 15)

        self.assertEqual(
            url,
            "https://crix-api-endpoint.upbit.com/v1/crix/candles/minutes/15?code=CRIX.UPBIT.KRW-ETH&count=400&",
        )

    def test_normalize_candles_returns_stable_columns(self):
        rows = data_history.normalize_candles(
            [
                {
                    "candleDateTimeKst": "2026-05-30T10:00:00",
                    "openingPrice": 1,
                    "highPrice": 2,
                    "lowPrice": 0.5,
                    "tradePrice": 1.5,
                    "candleAccTradeVolume": 100,
                    "candleAccTradePrice": 150,
                }
            ]
        )

        self.assertEqual(
            rows,
            [
                {
                    "Time": "2026-05-30T10:00:00",
                    "OpeningPrice": 1,
                    "HighPrice": 2,
                    "LowPrice": 0.5,
                    "TradePrice": 1.5,
                    "CandleAccTradeVolume": 100,
                    "CandleAccTradePrice": 150,
                }
            ],
        )

    def test_collect_history_omits_empty_downloads(self):
        with tempfile.TemporaryDirectory() as tmp:
            with patch.object(data_history, "fetch_candles", return_value=[]):
                files = data_history.collect_history(
                    coins=["BTC"],
                    time_units=["days"],
                    minute_units=[],
                    output_dir=tmp,
                )

            self.assertEqual(files, [])
            self.assertFalse((Path(tmp) / "BTC_KRW_days.csv").exists())


if __name__ == "__main__":
    unittest.main()
