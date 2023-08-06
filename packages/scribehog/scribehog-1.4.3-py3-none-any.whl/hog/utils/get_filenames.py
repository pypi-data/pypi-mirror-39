import os
from typing import List, Tuple, Optional

from hog.const import SCRIBE_ROOT, TIMESTAMP_LENGTH_IN_FILENAME


class NoFileMatchesAbsoluteSpecifierException(Exception):
    pass


def list_logfiles(directory: str) -> List[str]:
    return list(
        filter(
            lambda filename: not filename.endswith("_current"), os.listdir(directory)
        )
    )


def get_filenames(logcategory: str, interval: str) -> List[str]:
    filenames = sorted(list_logfiles(SCRIBE_ROOT + "/" + logcategory))
    return select_filenames_for_interval(filenames, interval)


def select_filenames_for_interval(filenames: List[str], interval: str) -> List[str]:
    if ":" in interval:
        start_index, end_index = _get_indexes_for_interval(
            filenames, *interval.split(":")
        )
        return filenames[start_index:end_index]
    else:
        index = _get_index_for_single(filenames, interval)
        return [filenames[index]]


def _get_indexes_for_interval(
    filenames: List[str], start_specifier: str, end_specifier: str
) -> Tuple[Optional[int], Optional[int]]:
    start_index = (
        _get_index_for_single(filenames, start_specifier)
        if start_specifier != ""
        else None
    )
    end_index = (
        _get_index_for_single(filenames, end_specifier) + 1
        if end_specifier != ""
        else None
    )
    if end_index == 0:
        end_index = None
    return start_index, end_index


def _get_index_for_single(filenames: List[str], specifier: str) -> int:
    return (
        _get_index_for_relative_single(specifier)
        if specifier.startswith("-")
        else _get_index_for_absolute_single(filenames, specifier)
    )


def _get_index_for_relative_single(specifier: str) -> int:
    return int(specifier)


def _get_index_for_absolute_single(filenames: List[str], specifier: str) -> int:
    filenames_and_slugs = [
        (filename, _get_slug_for_filename(filename)) for filename in filenames
    ]
    for index, (filaneme, slug) in enumerate(reversed(filenames_and_slugs)):
        if slug.endswith(specifier):
            return -index - 1
    else:
        raise NoFileMatchesAbsoluteSpecifierException


def _get_slug_for_filename(filename: str) -> str:
    return (
        filename.replace("_", "-")
        .replace(".gz", "")
        .replace("000", "")[-TIMESTAMP_LENGTH_IN_FILENAME:]
    )
