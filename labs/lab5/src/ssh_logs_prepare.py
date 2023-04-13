import re
import time
from collections import namedtuple
import datetime

PATTERN = re.compile("(?P<date>\w+ \d{1,2} \d{2}:\d{2}:\d{2}) "
                     "(?P<host>\w+) sshd\[(?P<pid>\d+)]: (?P<message>.+)")

log_entry = namedtuple("SSH_Entry", "date host pid message")


def parse_entry(entry):
    match = re.match(PATTERN, entry)
    return log_entry(date=datetime.datetime.strptime(match.group('date'), "%b %d %H:%M:%S"),
                     host=match.group('host'),
                     pid=int(match.group('pid')),
                     message=match.group('message'))