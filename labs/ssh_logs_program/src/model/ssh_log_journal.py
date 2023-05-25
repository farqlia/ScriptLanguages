import abc
from datetime import datetime
import ipaddress
from ipaddress import IPv4Address, AddressValueError

from labs.ssh_logs_program.src.model.ssh_log_entry import SSHLogEntry
import labs.ssh_logs_program.src.model.log_factory as log_factory
from typing import Iterable, List, Union, Any, Callable, Optional


# Subclasses are responsible for providing concrete subclass instances
# So we basically have two parallel hierarchies

# Zewnetrzna klasa kreatora


class LogJournal(abc.ABC):

    @abc.abstractmethod
    def append(self, value: str, creator: log_factory.LogCreator) -> bool:
        return False


class SSHLogJournal(LogJournal):

    def __init__(self) -> None:
        self.container: List[SSHLogEntry] = []
        self.index: int = -1

    def append(self, value: str, creator: log_factory.LogCreator) -> bool:
        instance: Optional[SSHLogEntry] = creator.create(value)
        is_valid: bool = instance is not None and instance.validate()
        if is_valid:
            self.container.append(instance)   # type: ignore
        return is_valid

    @staticmethod
    def _new_journal(items: Iterable[SSHLogEntry]) -> 'SSHLogJournal':
        new_journal: SSHLogJournal = SSHLogJournal()
        for item in items:
            new_journal.container.append(item)
        return new_journal

    def filter_for_ip(self, ipv4_address: Union[IPv4Address, str]) -> Union[List[Any], 'SSHLogJournal']:
        try:
            _ipv4_address: IPv4Address = IPv4Address(ipv4_address)
            return self.filter(lambda l: l.get_ipv4_address() == _ipv4_address)
        except AddressValueError:
            return []

    def filter(self, filter_method: Callable[[SSHLogEntry], bool]) -> 'SSHLogJournal':
        return SSHLogJournal._new_journal(list(filter(filter_method, self.container)))

    def __len__(self) -> int:
        return len(self.container)

    def __iter__(self) -> 'SSHLogJournal':
        self.index = -1
        return self

    def __next__(self) -> SSHLogEntry:
        if self.index + 1 == len(self.container):
            raise StopIteration
        self.index += 1
        return self.container[self.index]

    def __contains__(self, item: Any) -> bool:
        return item in self.container

    def __getitem__(self, index: Union[int, IPv4Address, datetime, slice]) \
            -> Union[SSHLogEntry, 'SSHLogJournal']:
        journal_or_instance: Union[SSHLogJournal, SSHLogEntry]
        if isinstance(index, slice):
            if isinstance(index.start, IPv4Address) or isinstance(index.stop, IPv4Address):
                start_address: IPv4Address = ipaddress.IPv4Address("0.0.0.0") if index.start is None else index.start
                stop_address: IPv4Address = ipaddress.IPv4Address("255.255.255.255") if index.stop is None else index.stop
                journal_or_instance = self.filter(lambda ssh_log: ssh_log.has_ip
                and start_address <= ssh_log.get_ipv4_address() < stop_address)     # type: ignore
            elif isinstance(index.start, datetime) or isinstance(index.stop, datetime):
                start_dt: datetime = datetime.min if index.start is None else index.start
                stop_dt: datetime = datetime.max if index.stop is None else index.stop
                journal_or_instance = self.filter(lambda ssh_log: start_dt <= ssh_log.date < stop_dt)
            else:
                journal_or_instance = self._new_journal([self.container[i] for i
                                                         in range(*index.indices(len(self.container)))])
        else:
            if isinstance(index, IPv4Address):
                journal_or_instance = self.filter(lambda ssh_log: ssh_log.has_ip and ssh_log.get_ipv4_address() == index)
            elif isinstance(index, datetime):
                journal_or_instance = self.filter(lambda ssh_log: ssh_log.date == index)
            else:
                journal_or_instance = self.container[index]
        return journal_or_instance
