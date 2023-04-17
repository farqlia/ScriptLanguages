import re
import time
from collections import namedtuple
import datetime


class Parser:

    PATTERN = re.compile("(?P<date>\w+\s+\d{1,2}\s+\d{2}:\d{2}:\d{2})\s+"
                     "(?P<host>\w+)\s+sshd\[(?P<pid>\d+)]:\s+(?P<message>.+)")

    log_entry = namedtuple("SSH_Entry", "date host pid message")

    def __init__(self):
        self.curr_year = 2022
        self.set_year = False

    def get_date(self, match):
        date = datetime.datetime.strptime(match.group('date'), "%b %d %H:%M:%S")

        if date.month == 1 and not self.set_year:
            self.curr_year += 1
            self.set_year = True

        date = datetime.datetime(year=self.curr_year, month=date.month, day=date.day,
                                 minute=date.minute, hour=date.hour, second=date.second)
        return date

    def frmt(self, log: log_entry, length=30):
        return f"{log.date.strftime('%d-%m-%y, %H:%M:%S')}, [{log.pid}] - {log.message[:length]} [...]"

    def parse_entry(self, entry):
        match = re.match(Parser.PATTERN, entry)

        if not match:
            raise ValueError(f"Couldn't parse: {entry}")

        return Parser.log_entry(date=self.get_date(match),
                                host=match.group('host'),
                                pid=int(match.group('pid')),
                                message=match.group('message'))