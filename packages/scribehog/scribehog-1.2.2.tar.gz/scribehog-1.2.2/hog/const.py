from os import environ

QUERY_RE_PATTERN = r"^\w+(-\w+)*$"
INTERVAL_RE_PATTERN = r"^(-?\d+(-\d+)*)?:?(-?\d+(-\d+)*)?$"
SCRIBE_ROOT = environ.get("SCRIBE_ROOT", "/mnt/scribe/")
TIMESTAMP_LENGTH_IN_FILENAME = 16
