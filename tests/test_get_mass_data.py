import unittest

import get_mass_data


class GetMassDataTest(unittest.TestCase):
    def test_resolve_interval_aliases(self):
        self.assertEqual(get_mass_data.resolve_interval("m1"), "minutes1")
        self.assertEqual(get_mass_data.resolve_interval("m240"), "minutes240")
        self.assertEqual(get_mass_data.resolve_interval("d"), "days")

    def test_resolve_interval_rejects_unknown_alias(self):
        with self.assertRaisesRegex(ValueError, "Unsupported interval"):
            get_mass_data.resolve_interval("hourly")


if __name__ == "__main__":
    unittest.main()
