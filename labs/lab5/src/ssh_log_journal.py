import abc
import datetime
import ipaddress

import labs.lab5.src.ssh_log_entry as ssh_log_entry
from ipaddress import IPv4Address, AddressValueError

# Subclasses are responsible for providing concrete subclass instances
# So we basically have two parallel hierarchies

# Zewnetrzna klasa kreatora


class SSHLogJournal(abc.ABC):

    @abc.abstractmethod
    def _make_instance(self, value):
        return None

    def __init__(self):
        self.container = []
        self.index = -1

    def append(self, value):
        instance = self._make_instance(value)
        is_valid = instance is not None and instance.validate()
        if is_valid:
            self.container.append(instance)
        return is_valid

    def filter_for_ip(self, ipv4_address):
        try:
            ipv4_address = IPv4Address(ipv4_address)
            return self.filter(lambda l: l.get_ipv4_address() == ipv4_address)
        except AddressValueError:
            return []

    def filter(self, filter_method):
        return list(filter(filter_method, self.container))

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
        if isinstance(index, slice):
            if isinstance(index.start, IPv4Address) or isinstance(index.stop, IPv4Address):
                start = ipaddress.IPv4Address("0.0.0.0") if index.start is None else index.start
                stop = ipaddress.IPv4Address("255.255.255.255") if index.stop is None else index.stop
                return list(filter(lambda ssh_log: ssh_log.has_ip and start <= ssh_log.get_ipv4_address() < stop,
                                   self.container))
            elif isinstance(index.start, datetime.datetime) or isinstance(index.stop, datetime.datetime):
                start = datetime.datetime.min if index.start is None else index.start
                stop = datetime.datetime.max if index.stop is None else index.stop
                return list(filter(lambda ssh_log: start <= ssh_log.date < stop, self.container))
            else:
                return [self.container[i] for i in range(*index.indices(len(self.container)))]
        else:
            if isinstance(index, IPv4Address):
                return list(filter(lambda ssh_log: ssh_log.has_ip and ssh_log.get_ipv4_address() == index,
                                   self.container))
            elif isinstance(index, datetime.datetime):
                return list(filter(lambda ssh_log: ssh_log.date == index, self.container))
            else:
                return self.container[index]


class AcceptedPasswordJournal(SSHLogJournal):

    def _make_instance(self, value):
        return ssh_log_entry.AcceptedPassword(value)


class OtherJournal(SSHLogJournal):

    def _make_instance(self, value):
        return ssh_log_entry.Other(value)