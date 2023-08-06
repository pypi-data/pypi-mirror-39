#!/usr/bin/env python3
from hog.utils.get_logcategory import list_logcategories
from hog.utils.verify_selected_logfiles import verify_selected_logfiles
from hog.wrapped import (
    wrapped_parse_args,
    wrapped_get_logcategory,
    wrapped_get_filenames,
    wrapped_print_logs,
)


def main() -> None:
    args = wrapped_parse_args()
    logcategories = list_logcategories()
    logcategory = wrapped_get_logcategory(
        args.logcategory, logcategories, args.is_verbose
    )
    filenames = wrapped_get_filenames(logcategory, args.interval, args.is_verbose)
    should_print_logs = verify_selected_logfiles() if args.should_verify else True
    if should_print_logs:
        wrapped_print_logs(logcategory, filenames, args.is_verbose)


if __name__ == "__main__":
    main()
