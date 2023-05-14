import re
from enum import Enum, auto
from ipaddress import ip_address

from labs.ssh_logs_program.src.model.ssh_logs_prepare import *

ip_part = ""
IPV4_PATTERN = re.compile(r"\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}")
# Don't want to catch ruser and user authentication
# |for (?<!invalid user )[\w\-.]+
USER_PATTERN = re.compile(r"((?<=[^r]user[\s=])(?!authentication)\s*[\w\-.]+|root)")
USER_PATTERN_2 = re.compile(r"for ([\w\-.]+)")

PORT_PATTERN = re.compile(r"port (\d+)")
# error: [\w\s:.]+:(?P<cause>\w+)
ERROR_CAUSE_PATTERN = re.compile(r"error: (?P<event>received disconnect|connect_to)[\w\s:.]+: (?P<cause>[\w\s]+)")

ACCEPTED_PASSWORD_PATTERN = re.compile(r"Accepted password for (?P<user>\w+) from (?P<ip>\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}) port (?P<port>\d+) ssh2")

FAILED_PASSWORD_PATTERN = re.compile(r"Failed password for (?P<user>\w+) from (?P<ip>\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}) port (?P<port>\d+) ssh2")

ERROR_PATTERN = re.compile(r"error: (?:Received disconnect from|connect_to) (?P<ip>\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})")


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
    for match in matches:
        try:
            ip_address(match)
        except ValueError:
            return None
    return matches


def get_user_from_log(entry):
    match = re.search(USER_PATTERN, entry.message)
    if not match:
        match = re.search(USER_PATTERN_2, entry.message)
    return match.group(1).strip() if match else None


def filter_user_logs(user, ssh_logs):
    return list(filter(lambda e: get_user_from_log(e) == user,
                ssh_logs))


def get_port(entry):
    match = re.search(PORT_PATTERN, entry.message)
    return int(match.group(1)) if match else None


def get_error_cause(entry):
    match = re.search(ERROR_CAUSE_PATTERN, entry.message.lower())
    if match:
        if match.group('event') == 'connect_to':
            return "connection: " + match.group('cause')
        else:
            return match.group('event') + ": " + match.group('cause').strip()

    return ""


def get_message_type(entry):

    message = entry.message.lower().strip()

    for k, v in MESSAGE_PATTERNS:
        if v.search(message):
            return k
