import abc
import datetime
import ipaddress
from ipaddress import IPv4Address, AddressValueError

import labs.ssh_logs_program.src.model.ssh_log_entry as ssh_log_entry
import labs.ssh_logs_program.src.model.log_factory as log_factory
from typing import Sequence

# Subclasses are responsible for providing concrete subclass instances
# So we basically have two parallel hierarchies

# Zewnetrzna klasa kreatora


class LogJournal(abc.ABC):

    def append(self, value, creator):
        pass


class SSHLogJournal(LogJournal):

    def __init__(self):
        self.container = []
        self.index = -1

    def append(self, value, creator: log_factory.LogCreator):
        instance = creator.create(value)
        is_valid = instance is not None and instance.validate()
        if is_valid:
            self.container.append(instance)
        return is_valid

    @staticmethod
    def _new_journal(items):
        new_journal = SSHLogJournal()
        for item in items:
            new_journal.container.append(item)
        return new_journal

    def filter_for_ip(self, ipv4_address):
        try:
            ipv4_address = IPv4Address(ipv4_address)
            return self.filter(lambda l: l.get_ipv4_address() == ipv4_address)
        except AddressValueError:
            return []

    def filter(self, filter_method):
        return SSHLogJournal._new_journal(list(filter(filter_method, self.container)))

    def __len__(self):
        return len(self.container)

    def __iter__(self):
        self.index = -1
        return self

    def __getattr__(self, item):
        return self.container[item]

    def __next__(self):
        if self.index + 1 == len(self.container):
            raise StopIteration
        self.index += 1
        return self.container[self.index]

    def __contains__(self, item):
        return item in self.container

    def __getitem__(self, index):
        subset = None
        if isinstance(index, slice):
            if isinstance(index.start, IPv4Address) or isinstance(index.stop, IPv4Address):
                start = ipaddress.IPv4Address("0.0.0.0") if index.start is None else index.start
                stop = ipaddress.IPv4Address("255.255.255.255") if index.stop is None else index.stop
                subset = list(filter(lambda ssh_log: ssh_log.has_ip and start <= ssh_log.get_ipv4_address() < stop,
                                   self.container))
            elif isinstance(index.start, datetime.datetime) or isinstance(index.stop, datetime.datetime):
                start = datetime.datetime.min if index.start is None else index.start
                stop = datetime.datetime.max if index.stop is None else index.stop
                subset = list(filter(lambda ssh_log: start <= ssh_log.date < stop, self.container))
            else:
                subset = [self.container[i] for i in range(*index.indices(len(self.container)))]
        else:
            if isinstance(index, IPv4Address):
                subset = list(filter(lambda ssh_log: ssh_log.has_ip and ssh_log.get_ipv4_address() == index,
                                   self.container))
            elif isinstance(index, datetime.datetime):
                subset = list(filter(lambda ssh_log: ssh_log.date == index, self.container))
            else:
                subset = self.container[index]
        return SSHLogJournal._new_journal(subset) if isinstance(subset, list) else subset