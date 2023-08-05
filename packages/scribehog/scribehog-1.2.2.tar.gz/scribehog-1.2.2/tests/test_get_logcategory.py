import unittest
from itertools import permutations

from utils.get_logcategory import (
    get_logcategory,
    NoLogcategoryFoundException,
    MultipleLogcategoriesFoundException,
)
from .data import mock_logcategories


class GetLogcategoryTestCase(unittest.TestCase):
    def test_no_match(self) -> None:
        with self.assertRaises(NoLogcategoryFoundException):
            get_logcategory("cheeseshop", [])

    def test_exact_match(self) -> None:
        result = get_logcategory("cheeseshop", mock_logcategories)
        self.assertEqual(result, "cheeseshop")

    def test_intelligent_match(self) -> None:
        result = get_logcategory("cheeseshop-d-b", mock_logcategories)
        self.assertEqual(result, "cheeseshop_danish_blue")

    def test_word_order_is_irrelevant(self) -> None:
        queries = [
            "{x}-{y}-{z}".format(x=x, y=y, z=z)
            for (x, y, z) in list(permutations(["c", "b", "d"]))
        ]
        results = [get_logcategory(query, mock_logcategories) for query in queries]
        self.assertTrue(all(result == "cheeseshop_danish_blue" for result in results))

    def test_underqualified_name_raises(self) -> None:
        with self.assertRaises(MultipleLogcategoriesFoundException):
            get_logcategory("che", ["cheese", "cheddar"])
