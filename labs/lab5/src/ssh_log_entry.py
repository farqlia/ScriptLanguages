import abc
from ipaddress import IPv4Address
from labs.lab5.src.ssh_logs_prepare import Parser
import labs.lab5.src.regex_ssh_utilis as regex_ssh_utils

parser = Parser()


# ABC - Abstract Base Classes
class SSHLogEntry(abc.ABC):

    @abc.abstractmethod
    def validate(self):
        return False

    def __init__(self, entry):
        entry_log = parser.parse_entry(entry)
        self._raw_log = entry
        self.host = entry_log.host
        self.pid = entry_log.pid
        self.message = entry_log.message
        self.date = entry_log.date
        self.ipv4_address = regex_ssh_utils.get_ipv4s_from_log(entry_log)
        self.ipv4_address = self.ipv4_address[0] if self.ipv4_address else None

        # add parsing ipv4 address

    @property
    def raw_log(self):
        return self._raw_log

    @property
    def has_ip(self):
        return self.ipv4_address is not None

    def reconstruct(self):
        return [self.date, self.host, self.pid, self.message]

    def get_ipv4_address(self):
        return IPv4Address(self.ipv4_address) if self.ipv4_address else None

    def __repr__(self):
        return f"{self.date.strftime('%b %d %H:%M:%S')} {self.host} sshd[{self.pid}]: {self.message}"

    def __eq__(self, other):
        result = other.host == self.host and other.pid == self.pid \
                 and other.message == self.message and self.date == other.date and self.ipv4_address == other.ipv4_address
        return result

    def __lt__(self, other):
        return self.date < other.date

    def __gt__(self, other):
        return self.date > other.date


class AcceptedPassword(SSHLogEntry):

    def __init__(self, entry):
        super().__init__(entry)
        match = regex_ssh_utils.ACCEPTED_PASSWORD_PATTERN.match(self.message)
        self.user = match.group("user") if match else None
        self.port = int(match.group("port")) if match else None

    def validate(self):
        return self.user is not None and self.port is not None and self == AcceptedPassword(self.raw_log)

    def __eq__(self, other):
        return super(AcceptedPassword, self).__eq__(other) and self.user == other.user and self.port == other.port


class FailedPassword(SSHLogEntry):

    def __init__(self, entry):
        super().__init__(entry)
        match = regex_ssh_utils.FAILED_PASSWORD_PATTERN.search(self.message)
        self.user = match.group("user") if match else None
        self.port = int(match.group("port")) if match else None

    def validate(self):
        return self.user is not None and self.port is not None and self == FailedPassword(self.raw_log)

    def __eq__(self, other):
        return super(FailedPassword, self).__eq__(other) and self.user == other.user and self.port == other.port


class Error(SSHLogEntry):

    def __init__(self, entry):
        super().__init__(entry)
        self.cause = regex_ssh_utils.get_error_cause(self)

    def validate(self):
        return self.cause is not None and self == Error(self.raw_log)

    def __eq__(self, other):
        return super(Error, self).__eq__(other) and self.cause == other.cause


class Other(SSHLogEntry):

    def __init__(self, entry):
        super().__init__(entry)

    def validate(self):
        return True
