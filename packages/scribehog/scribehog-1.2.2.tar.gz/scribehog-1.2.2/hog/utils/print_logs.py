import gzip
from typing import List
from os.path import join
from signal import signal, SIGPIPE, SIG_DFL

from hog.const import SCRIBE_ROOT

signal(SIGPIPE, SIG_DFL)


def print_logs(logcategory: str, filenames: List[str]) -> None:
    # TODO: test the "replace" mechanism for UnicodeDecodeError resilience
    for filename in filenames:
        if filename.endswith(".gz"):
            with gzip.open(
                join(SCRIBE_ROOT, logcategory, filename), mode="rt", errors="replace"
            ) as file:
                for line in filter(
                    lambda current_line: current_line.strip() != "",
                    file.read().split("\n"),
                ):
                    print(line)
        else:
            with open(
                join(SCRIBE_ROOT, logcategory, filename), errors="replace"
            ) as file:
                print(file.read().rstrip("\n"))
