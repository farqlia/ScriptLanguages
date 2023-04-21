import abc
from ipaddress import IPv4Address
from labs.lab5.src.ssh_logs_prepare import Parser
import labs.lab5.src.regex_ssh_utilis as regex_ssh_utils

parser = Parser()


# ABC - Abstract Base Classes
class SSHLogEntry(abc.ABC):

    @abc.abstractmethod
    def validate(self, value):
        return False

    def __init__(self, entry):
        entry_log = parser.parse_entry(entry)
        self.host = entry_log.host
        self.pid = entry_log.pid
        self._message = entry_log.message
        self.date = entry_log.date
        self.ipv4_address = regex_ssh_utils.get_ipv4s_from_log(entry_log)

        # add parsing ipv4 address

    @property
    def message(self):
        return self._message

    @property
    def has_ip(self):
        return self.ipv4_address is not None

    def reconstruct(self):
        return f"{self.date.strftime('%d-%m-%y, %H:%M:%S')} @{self.host} [{self.pid}]: {self.message}"

    def get_ipv4_address(self):
        return IPv4Address(self.ipv4_address[0]) if self.ipv4_address else None

    def __repr__(self):
        return f"{self.date.strftime('%b %d %H:%M:%S')} {self.host} sshd[{self.pid}]: {self._message}"

    def __eq__(self, other):
        return other.host == self.host and other.pid == self.pid \
               and other.message == self.message and self.date == other.date and self.ipv4_address == other.ipv4_address

    def __lt__(self, other):
        return self.date < other.date and self.pid == other.pid

    def __gt__(self, other):
        return


class AcceptedPassword(SSHLogEntry):

    def __init__(self, entry):
        super().__init__(entry)
        self.user = regex_ssh_utils.get_user_from_log(self)
        self.port = regex_ssh_utils.get_port(self)

    def validate(self, value):
        return value.lower().startwith("Accepted password")


class FailedPassword(SSHLogEntry):

    def __init__(self, entry):
        super().__init__(entry)
        self.user = regex_ssh_utils.get_user_from_log(self)
        self.port = regex_ssh_utils.get_port(self)

    def validate(self, value):
        return False


class Error(SSHLogEntry):

    def __init__(self, entry):
        super().__init__(entry)
        self.cause = regex_ssh_utils.get_error_cause(self)

    def validate(self, value):
        return False


class Other(SSHLogEntry):

    def __init__(self, entry):
        super().__init__(entry)

    def validate(self, value):
        return True