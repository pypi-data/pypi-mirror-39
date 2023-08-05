#!/usr/bin/env python3
from hog.utils.get_logcategory import list_logcategories
from hog.utils.print_logs import print_logs
from hog.wrapped import (
    wrapped_parse_args,
    wrapped_get_logcategory,
    wrapped_get_filenames,
)


def main() -> None:
    args = wrapped_parse_args()
    logcategories = list_logcategories()
    logcategory = wrapped_get_logcategory(
        args.logcategory, logcategories, args.is_verbose
    )
    filenames = wrapped_get_filenames(logcategory, args.interval, args.is_verbose)
    print_logs(logcategory, filenames)


if __name__ == "__main__":
    main()
