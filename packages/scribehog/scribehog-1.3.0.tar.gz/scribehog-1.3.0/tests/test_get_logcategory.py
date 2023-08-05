import unittest
from itertools import permutations

from utils.get_logcategory import (
    get_logcategory,
    NoLogcategoryFoundException,
    MultipleLogcategoriesFoundException,
    has_exact_word_match,
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

    def test_multiple_matches_exact_word_match_wins(self) -> None:
        result = get_logcategory(
            "cheese-b-c", ["cheese_bravo_charlie", "cheeseshop_bravo_charlie"]
        )
        self.assertEqual(result, "cheese_bravo_charlie")


class HasExactWordMatchTestCase(unittest.TestCase):
    def test_single_word_matches(self) -> None:
        self.assertTrue(has_exact_word_match("alpha", ["alpha"]))

    def test_multiple_words_no_exact_match(self) -> None:
        self.assertFalse(
            has_exact_word_match("alpha_bravo_charlie", ["br", "al", "ch"])
        )

    def test_multiple_words_one_exact_match(self) -> None:
        self.assertTrue(
            has_exact_word_match("alpha_bravo_charlie", ["bravo", "ch", "al"])
        )

    def test_multiple_words_multiple_exact_matches(self) -> None:
        self.assertTrue(
            has_exact_word_match("alpha_bravo_charlie", ["bravo", "al", "charlie"])
        )
