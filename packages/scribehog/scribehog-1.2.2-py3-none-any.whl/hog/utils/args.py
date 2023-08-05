import argparse
import re

from hog.const import QUERY_RE_PATTERN, INTERVAL_RE_PATTERN


def parse_args() -> argparse.Namespace:
    parser = _setup_parser()
    args = _parse_args_intelligently(parser)
    if _are_args_valid(args.logcategory, args.interval):
        return args
    else:
        raise argparse.ArgumentError(argument=None, message="Invalid args")


def _setup_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="hog", add_help=False)
    parser.add_argument(
        "-v",
        help="verbose logging for debug purposes",
        dest="is_verbose",
        action="store_true",
        default=False,
    )
    parser.add_argument(
        "logcategory", help="glob-like string to specify the log category"
    )
    parser.add_argument(
        "interval",
        nargs="?",
        default="-1",
        help="specify which log files should be read",
    )
    return parser


def _parse_args_intelligently(parser: argparse.ArgumentParser) -> argparse.Namespace:
    """Parse arguments, including complex interval specifiers

    argparse can't parse parameters that begin with a dash, eg. interval
    queries such as -1: as it tries to identify them as optional argument
    names because of the leading dash. Workaround is to parse only the
    known args and rescue the lost interval specifier parameter from the
    unkonwn args list.
    """
    args, unknown_args = parser.parse_known_args()
    if len(unknown_args) == 1:
        args.interval = unknown_args[0]
    return args


def _are_args_valid(logcategory: str, interval: str) -> bool:
    return (
        re.match(QUERY_RE_PATTERN, logcategory) is not None
        and re.match(INTERVAL_RE_PATTERN, interval) is not None
    )
