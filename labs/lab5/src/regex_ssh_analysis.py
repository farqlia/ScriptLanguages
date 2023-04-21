from enum import Enum, auto
from labs.lab5.src.ssh_logs_prepare import *

ip_part = "(\d|[1-9]\d|1\d{2}|2[0-4]\d|25[0-5])"
IPV4_PATTERN = re.compile(rf"({ip_part}\.{ip_part}\.{ip_part}\.{ip_part})[$|\D]")
# Don't want to catch ruser and user authentication
USER_PATTERN = re.compile(r"((?<=[^r]user[\s=])(?!authentication)\s*\w+|root)")


class MessageType(Enum):
    BREAK_IN_ATTEMPT = auto()
    INCORRECT_PASSWORD = auto()
    UNSUCCESSFUL_LOGIN = auto()
    INCORRECT_USERNAME = auto()
    CLOSED_CONNECTION = auto()
    SUCCESSFUL_LOGIN = auto()
    OTHER = auto()

    def format(self):
        return self.name.replace(r"\w+", " ").lower()


MESSAGE_PATTERNS = [(MessageType.BREAK_IN_ATTEMPT, re.compile("break[\s\-]?in")),
                    (MessageType.INCORRECT_PASSWORD, re.compile("failed password")),
                    (MessageType.CLOSED_CONNECTION, re.compile("connection closed|disconnect*?")),
                    (MessageType.UNSUCCESSFUL_LOGIN, re.compile("authentication failures?|input_userauth_request")),
                    (MessageType.INCORRECT_USERNAME, re.compile("invalid user")),
                    (MessageType.SUCCESSFUL_LOGIN, re.compile("^accepted")),
                    (MessageType.OTHER, re.compile(".*"))]


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

    message = entry.message.lower().strip()

    for k, v in MESSAGE_PATTERNS:
        if v.search(message):
            return k
