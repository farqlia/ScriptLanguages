import datetime
import re
from collections import namedtuple
from labs.ssh_logs_program.src.model.regex_ssh_utilis import get_user_from_str
from typing import NamedTuple

PATTERN = re.compile("(?P<date>\w+\s+\d{1,2}\s+\d{2}:\d{2}:\d{2})\s+"
                     "(?P<host>\w*)\s*sshd\[(?P<pid>\d+)]:\s+(?P<message>.+)")


class LogEntry(NamedTuple):
    date: datetime.datetime
    host: str
    pid: int
    message: str


class Parser:

    def __init__(self):
        self.curr_year = 2022
        self.set_year = False

    def get_date(self, match):
        date = datetime.datetime.strptime(match.group('date'), "%b %d %H:%M:%S")

        if date.month == 1:
            self.curr_year = 2023
        else:
            self.curr_year = 2022

        date = datetime.datetime(year=self.curr_year, month=date.month, day=date.day,
                                 minute=date.minute, hour=date.hour, second=date.second)
        return date

    def frmt(self, log: LogEntry, length=30):
        return f"{log.date.strftime('%d-%m-%y, %H:%M:%S')}, [{log.pid}] - {log.message[:length]} [...]"

    def parse_entry(self, entry):
        entry = entry.strip()
        match = re.match(PATTERN, entry)

        if not match:
            raise ValueError(f"Couldn't parse: {entry}")

        host = get_user_from_str(entry)

        return LogEntry(date=self.get_date(match),
                        host=host if host else "",
                        pid=int(match.group('pid')),
                        message=match.group('message'))
