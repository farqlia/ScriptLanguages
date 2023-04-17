import re
import time
from sys import getsizeof
from collections import namedtuple
import datetime
from enum import Enum
from labs.lab5.src.ssh_logs_prepare import *

IPV4_PATTERN = re.compile(r"\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}")
# Don't want to catch ruser and user authentication
USER_PATTERN = re.compile(r"((?<=[^r]user[\s=])(?!authentication)\s*\w+|root)")


MESSAGE_PATTERNS = [re.compile("break[\s\-]?in"),
                    re.compile("failed password"),
                    re.compile("authentication failures?|input_userauth_request"),
                    re.compile("invalid user"),
                    re.compile("connection closed|disconnect*?"),
                    re.compile("^accepted")]


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


def get_ipv4s_from_log(entry):
    matches = re.findall(IPV4_PATTERN, entry.message)
    return matches


def get_user_from_log(entry):
    match = re.search(USER_PATTERN, entry.message)
    return match.group(0).strip() if match else None


def filter_user_logs(user, ssh_logs):
    return list(filter(lambda e: get_user_from_log(e) == user,
                ssh_logs))


def get_message_type(entry):

    message = entry.message.lower()

    if re.search(MESSAGE_PATTERNS[MessageType.BREAK_IN_ATTEMPT.value], message):
        return MessageType.BREAK_IN_ATTEMPT
    elif re.search(MESSAGE_PATTERNS[MessageType.INCORRECT_PASSWORD.value], message):
        return MessageType.INCORRECT_PASSWORD
    elif re.search(MESSAGE_PATTERNS[MessageType.CLOSED_CONNECTION.value], message):
        return MessageType.CLOSED_CONNECTION
    elif re.search(MESSAGE_PATTERNS[MessageType.UNSUCCESSFUL_LOGIN.value], message):
        return MessageType.UNSUCCESSFUL_LOGIN
    elif re.search(MESSAGE_PATTERNS[MessageType.INCORRECT_USERNAME.value], message):
        return MessageType.INCORRECT_USERNAME
    elif re.search(MESSAGE_PATTERNS[MessageType.SUCCESSFUL_LOGIN.value], message):
        return MessageType.SUCCESSFUL_LOGIN
    else:
        return MessageType.OTHER