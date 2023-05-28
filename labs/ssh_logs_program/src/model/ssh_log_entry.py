import abc
from ipaddress import IPv4Address

import labs.ssh_logs_program.src.model.regex_ssh_utilis as regex_ssh_utils
from labs.ssh_logs_program.src.model.ssh_logs_prepare import Parser, LogEntry
from datetime import datetime
from typing import List, Union, Tuple, Optional, NamedTuple
from re import Match

parser: Parser = Parser()


# ABC - Abstract Base Classes
class SSHLogEntry(abc.ABC):

    @abc.abstractmethod
    def validate(self) -> bool:
        return False

    def __init__(self, entry: str) -> None:
        entry_log: LogEntry = parser.parse_entry(entry)
        self._raw_log: str = entry
        self.host: str = entry_log.host
        self.pid: int = entry_log.pid
        self.message: str = entry_log.message
        self.date: datetime = entry_log.date
        ipv4_address: Optional[List[str]] = regex_ssh_utils.get_ipv4s_from_log(entry_log)
        self.ipv4_address: Optional[IPv4Address] = IPv4Address(ipv4_address[0]) if ipv4_address else None

        # add parsing ipv4 address

    @property
    def raw_log(self) -> str:
        return self._raw_log

    @property
    def has_ip(self) -> bool:
        return self.ipv4_address is not None

    def reconstruct(self) -> Tuple[datetime, str, int, str]:
        return self.date, self.host, self.pid, self.message

    def get_ipv4_address(self) -> Optional[IPv4Address]:
        return self.ipv4_address if self.ipv4_address else None

    def __str__(self) -> str:
        return self._raw_log

    def __repr__(self) -> str:
        return f"{self.date.strftime('%b %d %H:%M:%S')} sshd[{self.pid}]: {self.message}"

    def __eq__(self, other: object) -> bool:
        result = isinstance(other, SSHLogEntry) and other.host == self.host and other.pid == self.pid \
                 and other.message == self.message and self.date == other.date \
                 and self.ipv4_address == other.ipv4_address
        return result

    def __lt__(self, other: 'SSHLogEntry') -> bool:
        return self.date < other.date

    def __gt__(self, other: 'SSHLogEntry') -> bool:
        return self.date > other.date


class AcceptedPassword(SSHLogEntry):

    def __init__(self, entry: str) -> None:
        super().__init__(entry)
        match: Optional[Match[str]] = regex_ssh_utils.ACCEPTED_PASSWORD_PATTERN.match(self.message)
        self.port: Optional[int] = int(match.group("port")) if match else None

    def validate(self) -> bool:
        return self == AcceptedPassword(self.raw_log)

    def __eq__(self, other: object) -> bool:
        is_type: bool = isinstance(other, AcceptedPassword)
        if is_type:
            other_match: Optional[Match[str]] = regex_ssh_utils.ACCEPTED_PASSWORD_PATTERN.match(getattr(other, "message"))
            return other_match is not None and super(AcceptedPassword, self).__eq__(other) \
                   and self.port == int(other_match.group('port'))
        return False


class FailedPassword(SSHLogEntry):

    def __init__(self, entry: str) -> None:
        super().__init__(entry)
        match: Optional[Match[str]] = regex_ssh_utils.FAILED_PASSWORD_PATTERN.search(self.message)
        self.port: Optional[int] = int(match.group("port")) if match else None

    def validate(self) -> bool:
        return self == FailedPassword(self.raw_log)

    def __eq__(self, other: object) -> bool:
        is_type: bool = isinstance(other, FailedPassword)
        if is_type:
            other_match: Optional[Match[str]] = regex_ssh_utils.FAILED_PASSWORD_PATTERN.match(getattr(other, "message"))
            return other_match is not None and super(FailedPassword, self).__eq__(other) and self.port == int(
                other_match.group('port'))
        return False


class Error(SSHLogEntry):

    def __init__(self, entry: str) -> None:
        super().__init__(entry)
        self.cause: str = regex_ssh_utils.get_error_cause(self)

    def validate(self) -> bool:
        return self == Error(self.raw_log)

    def __eq__(self, other: object) -> bool:
        is_type: bool = isinstance(other, Error)
        if is_type:
            return super(Error, self).__eq__(other) and self.cause == regex_ssh_utils.get_error_cause(other)
        return False


class Other(SSHLogEntry):

    def __init__(self, entry: str) -> None:
        super().__init__(entry)

    def validate(self) -> bool:
        return True
