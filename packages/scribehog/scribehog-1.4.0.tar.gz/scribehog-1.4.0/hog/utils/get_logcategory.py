import os
from typing import List

from hog.const import SCRIBE_ROOT


class NoLogcategoryFoundException(Exception):
    pass


class MultipleLogcategoriesFoundException(Exception):
    def __init__(self, logcategories: List[str]) -> None:
        super().__init__()
        self.logcategories = logcategories
        self.count = len(logcategories)


class WordPrefixNotFoundException(Exception):
    pass


def list_logcategories() -> List[str]:
    return os.listdir(SCRIBE_ROOT)


def get_logcategory(query: str, logcategories: List[str]) -> str:
    query_words = query.split("-")
    logcategories_with_n_words = filter(
        lambda logcategory: len(_get_words_from_name(logcategory)) == len(query_words),
        logcategories,
    )
    matching_logcategories = list(
        filter(
            lambda logcategory: does_name_match_pattern(
                name=logcategory, pattern=query_words
            ),
            logcategories_with_n_words,
        )
    )
    if len(matching_logcategories) == 0:
        raise NoLogcategoryFoundException
    elif len(matching_logcategories) > 1:
        matching_logcategories_with_exact_word_match = list(
            filter(
                lambda logcategory: has_exact_word_match(logcategory, query_words),
                matching_logcategories,
            )
        )
        if len(matching_logcategories_with_exact_word_match) != 1:
            raise MultipleLogcategoriesFoundException(matching_logcategories)

    return matching_logcategories[0]


def does_name_match_pattern(name: str, pattern: List[str]) -> bool:
    words = _get_words_from_name(name)
    pattern_words_by_length = sorted(pattern, key=lambda w: -len(w))
    try:
        for pattern_word in pattern_words_by_length:
            words = get_word_list_without_matching_word(words, pattern_word)
    except WordPrefixNotFoundException:
        return False
    else:
        return True


def get_word_list_without_matching_word(
    word_list: List[str], word_prefix: str
) -> List[str]:
    for i, word in enumerate(word_list):
        if word.startswith(word_prefix):
            word_list_without_matching_word = word_list[:i] + word_list[i + 1 :]
            return word_list_without_matching_word
    raise WordPrefixNotFoundException()


def _get_words_from_name(name: str) -> List[str]:
    return name.replace("_", "-").split("-")


def has_exact_word_match(logcategory: str, query_words: List[str]) -> bool:
    words = _get_words_from_name(logcategory)
    for word in words:
        if word in query_words:
            return True
    return False
