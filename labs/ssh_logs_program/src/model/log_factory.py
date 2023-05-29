import labs.ssh_logs_program.src.model.ssh_log_entry as ssh_log_entry
from labs.ssh_logs_program.src.model.ssh_log_entry import SSHLogEntry, AcceptedPassword, FailedPassword, Error, Other
import abc
from typing import Union, Any, Optional, Protocol


class LogCreator(Protocol):

    @abc.abstractmethod
    def create(self, value: str) -> Optional[SSHLogEntry]:
        return None


class AcceptedPasswordCreator(LogCreator):

    def create(self, value: str) -> Optional[AcceptedPassword]:
        return ssh_log_entry.AcceptedPassword(value)


class FailedPasswordCreator(LogCreator):

    def create(self, value: str) -> Optional[FailedPassword]:
        return ssh_log_entry.FailedPassword(value)


class ErrorCreator(LogCreator):

    def create(self, value: str) -> Optional[Error]:
        return ssh_log_entry.Error(value)


class OtherCreator(LogCreator):

    def create(self, value: str) -> Optional[Other]:
        return ssh_log_entry.Other(value)