import unittest

from .data import mock_logfiles
from utils.get_filenames import (
    NoFileMatchesAbsoluteSpecifierException,
    select_filenames_for_interval,
)


class SelectFilenamesForRelativeIntervalTestCase(unittest.TestCase):
    def test_default_get_last_single(self) -> None:
        filenames = select_filenames_for_interval(["a", "b", "c"], "-1")
        self.assertEqual(filenames, ["c"])

    def test_get_relative_single(self) -> None:
        filenames = select_filenames_for_interval(["a", "b", "c"], "-2")
        self.assertEqual(filenames, ["b"])

    def test_get_relative_single_out_of_range(self) -> None:
        with self.assertRaises(Exception):
            select_filenames_for_interval(["a", "b", "c"], "-4")

    def test_get_relative_interval_fully_specified(self) -> None:
        filenames = select_filenames_for_interval(["a", "b", "c", "d", "e"], "-3:-2")
        self.assertEqual(filenames, ["c", "d"])

    def test_relative_interval_edge_case(self) -> None:
        filenames = select_filenames_for_interval(["a", "b", "c", "d", "e"], "-3:-1")
        self.assertEqual(filenames, ["c", "d", "e"])

    def test_get_relative_interval_open_left(self) -> None:
        filenames = select_filenames_for_interval(["a", "b", "c", "d", "e"], ":-2")
        self.assertEqual(filenames, ["a", "b", "c", "d"])

    def test_get_relative_interval_open_right(self) -> None:
        filenames = select_filenames_for_interval(["a", "b", "c", "d", "e"], "-3:")
        self.assertEqual(filenames, ["c", "d", "e"])

    def test_get_relative_interval_end_before_start_is_empty(self) -> None:
        filenames = select_filenames_for_interval(["a", "b", "c", "d", "e"], "-2:-3")
        self.assertEqual(filenames, [])


class SelectFilenamesForAbsoluteIntervalTestCase(unittest.TestCase):
    def test_get_absolute_single_one_digit_no_leading_zero(self) -> None:
        filenames = select_filenames_for_interval(mock_logfiles, "3")
        self.assertEqual(filenames, ["cheddar-2018-01-01_00023"])

    def test_get_absolute_single_one_digit_with_leading_zero(self) -> None:
        filenames = select_filenames_for_interval(mock_logfiles, "03")
        self.assertEqual(filenames, ["cheddar-2018-01-01_00003.gz"])

    def test_get_absolute_single_last(self) -> None:
        filenames = select_filenames_for_interval(mock_logfiles, "23")
        self.assertEqual(filenames, ["cheddar-2018-01-01_00023"])

    def test_get_absolute_single_gzip(self) -> None:
        filenames = select_filenames_for_interval(mock_logfiles, "21")
        self.assertEqual(filenames, ["cheddar-2018-01-01_00021.gz"])

    def test_get_absolute_single_gzip_by_day(self) -> None:
        filenames = select_filenames_for_interval(mock_logfiles, "31-21")
        self.assertEqual(filenames, ["cheddar-2017-12-31_00021.gz"])

    def test_get_absolute_single_gzip_by_month(self) -> None:
        filenames = select_filenames_for_interval(mock_logfiles, "12-31-21")
        self.assertEqual(filenames, ["cheddar-2017-12-31_00021.gz"])

    def test_get_absolute_single_gzip_by_stub_year(self) -> None:
        filenames = select_filenames_for_interval(mock_logfiles, "17-12-31-21")
        self.assertEqual(filenames, ["cheddar-2017-12-31_00021.gz"])

    def test_get_absolute_single_gzip_by_full_year(self) -> None:
        filenames = select_filenames_for_interval(mock_logfiles, "2017-12-31-21")
        self.assertEqual(filenames, ["cheddar-2017-12-31_00021.gz"])

    def test_get_invalid_absolute_single_raises(self) -> None:
        with self.assertRaises(NoFileMatchesAbsoluteSpecifierException):
            select_filenames_for_interval(mock_logfiles, "24")

    def test_get_absolute_interval_hour_to_hour(self) -> None:
        filenames = select_filenames_for_interval(mock_logfiles, "21:23")
        self.assertEqual(
            filenames,
            [
                "cheddar-2018-01-01_00021.gz",
                "cheddar-2018-01-01_00022",
                "cheddar-2018-01-01_00023",
            ],
        )

    def test_get_absolute_interval_end_before_start_is_empty(self) -> None:
        filenames = select_filenames_for_interval(mock_logfiles, "23:01")
        self.assertEqual(filenames, [])

    def test_get_absolute_interval_day_to_hour(self) -> None:
        filenames = select_filenames_for_interval(mock_logfiles, "31-23:01")
        self.assertEqual(
            filenames,
            [
                "cheddar-2017-12-31_00023.gz",
                "cheddar-2018-01-01_00000.gz",
                "cheddar-2018-01-01_00001.gz",
            ],
        )

    def test_get_absolute_interval_open_left(self) -> None:
        filenames = select_filenames_for_interval(mock_logfiles, ":01")
        self.assertEqual(
            filenames,
            [
                "cheddar-2017-12-31_00019.gz",
                "cheddar-2017-12-31_00020.gz",
                "cheddar-2017-12-31_00021.gz",
                "cheddar-2017-12-31_00022.gz",
                "cheddar-2017-12-31_00023.gz",
                "cheddar-2018-01-01_00000.gz",
                "cheddar-2018-01-01_00001.gz",
            ],
        )

    def test_get_absolute_interval_open_right(self) -> None:
        filenames = select_filenames_for_interval(mock_logfiles, "17:")
        self.assertEqual(
            filenames,
            [
                "cheddar-2018-01-01_00017.gz",
                "cheddar-2018-01-01_00018.gz",
                "cheddar-2018-01-01_00019.gz",
                "cheddar-2018-01-01_00020.gz",
                "cheddar-2018-01-01_00021.gz",
                "cheddar-2018-01-01_00022",
                "cheddar-2018-01-01_00023",
            ],
        )


class SelectFilenamesForMixedIntervalTestCase(unittest.TestCase):
    def test_get_relative_to_absolute_interval(self) -> None:
        filenames = select_filenames_for_interval(mock_logfiles, "-6:22")
        self.assertEqual(
            filenames,
            [
                "cheddar-2018-01-01_00018.gz",
                "cheddar-2018-01-01_00019.gz",
                "cheddar-2018-01-01_00020.gz",
                "cheddar-2018-01-01_00021.gz",
                "cheddar-2018-01-01_00022",
            ],
        )

    def test_get_absolute_to_relative_interval(self) -> None:
        filenames = select_filenames_for_interval(mock_logfiles, "17:-2")
        self.assertEqual(
            filenames,
            [
                "cheddar-2018-01-01_00017.gz",
                "cheddar-2018-01-01_00018.gz",
                "cheddar-2018-01-01_00019.gz",
                "cheddar-2018-01-01_00020.gz",
                "cheddar-2018-01-01_00021.gz",
                "cheddar-2018-01-01_00022",
            ],
        )
