import re
import time
from sys import getsizeof
from collections import namedtuple
from enum import Enum

PATTERN = re.compile("(?P<month>\w+) (?P<day>\d+) (?P<time>\d{2}:\d{2}:\d{2}) "
                     "(?P<host>\w+) sshd\[(?P<pid>\d+)]: (?P<message>.+)")

IPV4_PATTERN = re.compile(r"\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}")
# Don't want to catch ruser
USER_PATTERN = re.compile(r"((?<=[^r]user[\s=])\s*\w+|root)")

log_entry = namedtuple("SSH_Entry", "month_day time host pid message")


MESSAGE_PATTERNS = [re.compile("break[\s\-]?in"),
                    re.compile("failed password"),
                    re.compile("authentication failures?"),
                    re.compile("invalid user"),
                    re.compile("connection closed|disconnect"),
                    re.compile("accepted")]


class MessageType(Enum):
    BREAK_IN_ATTEMPT = 0
    INCORRECT_PASSWORD = 1
    UNSUCCESSFUL_LOGIN = 2
    INCORRECT_USERNAME = 3
    CLOSED_CONNECTION = 4
    SUCCESSFUL_LOGIN = 5
    OTHER = 6

    def format(self):
        return self.name.replace(r"\w+", " ").lower()


def parse_entry(entry):
    match = re.match(PATTERN, entry)
    return log_entry(month_day=f"{match.group('month')}-{match.group('day')}",
                     time=match.group('time'),
                     host=match.group('host'),
                     pid=int(match.group('pid')),
                     message=match.group('message'))


def get_ipv4s_from_log(entry: log_entry):
    matches = re.findall(IPV4_PATTERN, entry.message)
    return matches


def get_user_from_log(entry: log_entry):
    match = re.search(USER_PATTERN, entry.message)
    return match.group(0).strip() if match else None


def get_message_type(entry: log_entry):

    message = entry.message.lower()

    if re.search(MESSAGE_PATTERNS[MessageType.BREAK_IN_ATTEMPT.value], message):
        return MessageType.BREAK_IN_ATTEMPT
    elif re.search(MESSAGE_PATTERNS[MessageType.INCORRECT_PASSWORD.value], message):
        return MessageType.INCORRECT_PASSWORD
    elif re.search(MESSAGE_PATTERNS[MessageType.UNSUCCESSFUL_LOGIN.value], message):
        return MessageType.UNSUCCESSFUL_LOGIN
    elif re.search(MESSAGE_PATTERNS[MessageType.INCORRECT_USERNAME.value], message):
        return MessageType.INCORRECT_USERNAME
    elif re.search(MESSAGE_PATTERNS[MessageType.CLOSED_CONNECTION.value], message):
        return MessageType.CLOSED_CONNECTION
    elif re.search(MESSAGE_PATTERNS[MessageType.SUCCESSFUL_LOGIN.value], message):
        return MessageType.SUCCESSFUL_LOGIN
    else:
        return MessageType.OTHER
