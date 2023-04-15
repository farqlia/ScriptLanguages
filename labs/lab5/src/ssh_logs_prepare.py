import re
import time
from collections import namedtuple
import datetime

PATTERN = re.compile("(?P<date>\w+\s+\d{1,2}\s+\d{2}:\d{2}:\d{2})\s+"
                     "(?P<host>\w+)\s+sshd\[(?P<pid>\d+)]:\s+(?P<message>.+)")

log_entry = namedtuple("SSH_Entry", "date host pid message")


def parse_entry(entry):
    match = re.match(PATTERN, entry)

    if not match:
        raise ValueError(f"Couldn't parse: {entry}")

    return log_entry(date=datetime.datetime.strptime(match.group('date'), "%b %d %H:%M:%S"),
                     host=match.group('host'),
                     pid=int(match.group('pid')),
                     message=match.group('message'))