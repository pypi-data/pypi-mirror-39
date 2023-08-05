import unittest

from utils.get_logcategory import get_word_list_without_matching_word


class GetWordListWithoutMatchingWordTestCase(unittest.TestCase):
    word_list = ["alpha", "bravo", "charlie", "check"]

    def test_single_word_exact_match(self) -> None:
        result = get_word_list_without_matching_word(["alpha"], "alpha")
        self.assertEqual(result, [])

    def test_single_word_prefix_match(self) -> None:
        result = get_word_list_without_matching_word(["alpha"], "al")
        self.assertEqual(result, [])

    def test_multiple_words_exact_match_start_of_list(self) -> None:
        result = get_word_list_without_matching_word(self.word_list, "alpha")
        self.assertEqual(result, ["bravo", "charlie", "check"])

    def test_multiple_words_prefix_match_start_of_list(self) -> None:
        result = get_word_list_without_matching_word(self.word_list, "al")
        self.assertEqual(result, ["bravo", "charlie", "check"])

    def test_multiple_words_exact_match_inside_list(self) -> None:
        result = get_word_list_without_matching_word(self.word_list, "bravo")
        self.assertEqual(result, ["alpha", "charlie", "check"])

    def test_multiple_words_prefix_match_inside_list(self) -> None:
        result = get_word_list_without_matching_word(self.word_list, "bra")
        self.assertEqual(result, ["alpha", "charlie", "check"])

    def test_multiple_words_exact_match_end_of_list(self) -> None:
        result = get_word_list_without_matching_word(self.word_list, "check")
        self.assertEqual(result, ["alpha", "bravo", "charlie"])

    def test_multiple_words_prefix_match_end_of_list(self) -> None:
        result = get_word_list_without_matching_word(self.word_list, "che")
        self.assertEqual(result, ["alpha", "bravo", "charlie"])

    def test_multiple_words_ambigious_prefix(self) -> None:
        result = get_word_list_without_matching_word(self.word_list, "ch")
        self.assertTrue(
            any(
                [
                    result == ["alpha", "bravo", "charlie"],
                    result == ["alpha", "bravo", "check"],
                ]
            )
        )

    def test_multiple_words_unambigious_prefix(self) -> None:
        result = get_word_list_without_matching_word(self.word_list, "cha")
        self.assertEqual(result, ["alpha", "bravo", "check"])

    def test_empty_list_raises(self) -> None:
        with self.assertRaises(Exception):
            get_word_list_without_matching_word([], "alpha")

    def test_missing_word_raises(self) -> None:
        with self.assertRaises(Exception):
            get_word_list_without_matching_word(self.word_list, "delta")
