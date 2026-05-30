import os
import tempfile
import unittest
from unittest.mock import Mock, patch

import autotrading


class ApiKeyLoadingTest(unittest.TestCase):
    def setUp(self):
        self.env_patch = patch.dict(os.environ, {}, clear=True)
        self.env_patch.start()

    def tearDown(self):
        self.env_patch.stop()

    def test_load_api_keys_prefers_environment(self):
        os.environ["UPBIT_ACCESS_KEY"] = "env-access"
        os.environ["UPBIT_SECRET_KEY"] = "env-secret"

        keys = autotrading.load_api_keys(key_file="missing-key-file")

        self.assertEqual(keys, ("env-access", "env-secret"))

    def test_load_api_keys_reads_legacy_file(self):
        with tempfile.NamedTemporaryFile("w", delete=False) as key_file:
            key_file.write("file-access\nfile-secret\n")
            key_file_name = key_file.name

        try:
            keys = autotrading.load_api_keys(key_file=key_file_name)
        finally:
            os.unlink(key_file_name)

        self.assertEqual(keys, ("file-access", "file-secret"))

    def test_login_requires_pyupbit_dependency(self):
        os.environ["UPBIT_ACCESS_KEY"] = "env-access"
        os.environ["UPBIT_SECRET_KEY"] = "env-secret"

        with patch.object(autotrading, "pyupbit", None):
            with self.assertRaisesRegex(RuntimeError, "pyupbit"):
                autotrading.login()


class OrderApiTest(unittest.TestCase):
    def test_cancel_order_uses_given_uuid(self):
        key = Mock()

        autotrading.cancel_order(key, "order-uuid")

        key.cancel_order.assert_called_once_with("order-uuid")

    def test_legacy_cancle_order_alias_uses_given_uuid(self):
        key = Mock()

        autotrading.cancle_order(key, "legacy-uuid")

        key.cancel_order.assert_called_once_with("legacy-uuid")


class DataFrameSearchTest(unittest.TestCase):
    def test_search_dataframe_uses_requested_ticker(self):
        class TickerColumn:
            def __init__(self):
                self.compared_to = None

            def __eq__(self, ticker):
                self.compared_to = ticker
                return ["mask", ticker]

        class SearchableFrame:
            def __init__(self):
                self.ticker_column = TickerColumn()
                self.applied_mask = None

            def __getitem__(self, key):
                if key == "TICKER":
                    return self.ticker_column
                self.applied_mask = key
                return key

        df = SearchableFrame()

        result = autotrading.search_dataframe(df, "KRW-ETH")

        self.assertEqual(df.ticker_column.compared_to, "KRW-ETH")
        self.assertEqual(df.applied_mask, ["mask", "KRW-ETH"])
        self.assertEqual(result, ["mask", "KRW-ETH"])


class CurrentPriceTest(unittest.TestCase):
    def test_add_current_price_requires_pyupbit_dependency(self):
        with patch.object(autotrading, "pyupbit", None):
            with self.assertRaisesRegex(RuntimeError, "pyupbit"):
                autotrading.add_current_price("KRW-BTC", {})


if __name__ == "__main__":
    unittest.main()
