import argparse
from sys import stderr
from typing import List

from hog.utils.args import parse_args
from hog.utils.get_filenames import (
    get_filenames,
    NoFileMatchesAbsoluteSpecifierException,
)
from hog.utils.get_logcategory import (
    get_logcategory,
    NoLogcategoryFoundException,
    MultipleLogcategoriesFoundException,
)
from utils.print_logs import print_logs


def wrapped_parse_args() -> argparse.Namespace:
    try:
        args = parse_args()
    except argparse.ArgumentError as ex:
        print("ArgumentError: {}".format(ex), file=stderr)
        exit(1)

    if args.is_verbose:
        print("---hog logcategory specifier: {}".format(args.logcategory), file=stderr)
        print("---hog interval specifier: {}".format(args.interval), file=stderr)

    return args


def wrapped_get_logcategory(
    query: str, logcategories: List[str], is_verbose: bool
) -> str:
    try:
        logcategory = get_logcategory(query=query, logcategories=logcategories)
    except NoLogcategoryFoundException:
        print("No logcategory found for identifier '{}'".format(query), file=stderr)
        exit(1)
    except MultipleLogcategoriesFoundException as ex:
        print(
            "Multiple logcategories found for identifier '{}':".format(query),
            file=stderr,
        )
        print(
            "\n".join("- " + logcategory for logcategory in ex.logcategories[:10]),
            file=stderr,
        )
        if ex.count > 10:
            print("...and {} more".format(ex.count - 10))
        exit(1)

    if is_verbose:
        print("---hog logcategory: {}".format(logcategory), file=stderr)

    return logcategory


def wrapped_get_filenames(
    logcategory: str, interval: str, is_verbose: bool
) -> List[str]:
    try:
        filenames = get_filenames(logcategory, interval)
    except NoFileMatchesAbsoluteSpecifierException:
        print(
            "No file mathces the absolute specifier '{}'".format(interval), file=stderr
        )
        exit(1)

    if is_verbose:
        print("---hog filenames:", file=stderr)
        for filename in filenames:
            print(filename, file=stderr)

    return filenames


def wrapped_print_logs(
    logcategory: str, filenames: List[str], is_verbose: bool
) -> None:
    if is_verbose:
        print("---hog file contents:", file=stderr)
    print_logs(logcategory, filenames)
