import labs.ssh_logs_program.src.model.ssh_log_entry as ssh_log_entry
import abc


class LogCreator(abc.ABC):

    @abc.abstractmethod
    def create(self, value):
        return None


class AcceptedPasswordCreator(LogCreator):

    def create(self, value):
        return ssh_log_entry.AcceptedPassword(value)


class OtherCreator(LogCreator):

    def create(self, value):
        return ssh_log_entry.Other(value)