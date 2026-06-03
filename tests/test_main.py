import unittest
import pandas as pd
from pandas.testing import assert_series_equal

from app.docker.main import enrich_date


class TestEnrichDate(unittest.TestCase):

    def test_returns_day_difference(self):
        df = pd.DataFrame({
            "start_date": pd.to_datetime([
                "2024-01-01",
                "2024-01-10",
                "2024-02-01"
            ]),
            "end_date": pd.to_datetime([
                "2024-01-05",
                "2024-01-15",
                "2024-02-10"
            ])
        })

        result = enrich_date(df, "start_date", "end_date")

        expected = pd.Series([4, 5, 9])

        assert_series_equal(
            result.reset_index(drop=True),
            expected.reset_index(drop=True)
        )

    def test_same_day_returns_zero(self):
        df = pd.DataFrame({
            "start_date": pd.to_datetime(["2024-01-01"]),
            "end_date": pd.to_datetime(["2024-01-01"])
        })

        result = enrich_date(df, "start_date", "end_date")

        expected = pd.Series([0])

        assert_series_equal(
            result.reset_index(drop=True),
            expected.reset_index(drop=True)
        )

    def test_negative_difference(self):
        df = pd.DataFrame({
            "start_date": pd.to_datetime(["2024-01-05"]),
            "end_date": pd.to_datetime(["2024-01-01"])
        })

        result = enrich_date(df, "start_date", "end_date")

        expected = pd.Series([-4])

        assert_series_equal(
            result.reset_index(drop=True),
            expected.reset_index(drop=True)
        )


if __name__ == "__main__":
    unittest.main()