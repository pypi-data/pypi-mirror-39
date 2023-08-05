import unittest

from utils.get_logcategory import does_name_match_pattern


class DoesNameMatchPatternTestCase(unittest.TestCase):
    def test_single_word_exact_match(self) -> None:
        self.assertTrue(does_name_match_pattern(name="alpha", pattern=["alpha"]))

    def test_single_word_prefix_match(self) -> None:
        self.assertTrue(does_name_match_pattern(name="alpha", pattern=["al"]))

    def test_single_word_no_match(self) -> None:
        self.assertFalse(does_name_match_pattern(name="alpha", pattern=["bravo"]))

    def test_two_words_exact_match(self) -> None:
        self.assertTrue(
            does_name_match_pattern(name="alpha-bravo", pattern=["alpha", "bravo"])
        )

    def test_two_words_switched_match(self) -> None:
        self.assertTrue(
            does_name_match_pattern(name="alpha-bravo", pattern=["bravo", "alpha"])
        )

    def test_two_words_prefix_match(self) -> None:
        self.assertTrue(does_name_match_pattern(name="alpha-bravo", pattern=["a", "b"]))

    def test_two_words_switched_prefix_match(self) -> None:
        self.assertTrue(
            does_name_match_pattern(name="alpha-bravo", pattern=["br", "al"])
        )

    def test_two_words_no_match(self) -> None:
        self.assertFalse(
            does_name_match_pattern(name="alpha-bravo", pattern=["al", "ch"])
        )

    def test_several_words_specificity_beats_order(self) -> None:
        # the pattern should be sorted by length (longest ie. most specific first)
        # so that less specific prefixes don't remove the wrong word from the list
        # eg. "alph" should be checked first, lest "al" removes "alpha" leaving "alpine"
        self.assertTrue(
            does_name_match_pattern(
                name="alpha-bravo-alpine", pattern=["al", "br", "alph"]
            )
        )

    def test_dash_equals_underscore(self) -> None:
        self.assertTrue(
            all(
                does_name_match_pattern(name=name, pattern=["c", "b", "a"])
                for name in [
                    "alpha-bravo-charlie",
                    "alpha-bravo_charlie",
                    "alpha_bravo-charlie",
                    "alpha_bravo_charlie",
                ]
            )
        )
