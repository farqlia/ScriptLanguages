from os import access, R_OK
from pathlib import Path
from labs.ssh_logs_program.src.model.ssh_log_journal import LogJournal, SSHLogJournal
from labs.ssh_logs_program.src.model.log_factory import OtherCreator
import logging
import abc


class LogHandler(abc.ABC):

    def read_from_file(self, path) -> LogJournal:
        pass

    def is_correct_extension(self, path):
        pass

    def can_be_opened(self, path):
        return False


class SSHLogsHandler(LogHandler):

    def __init__(self):
        self.creator = OtherCreator()

    def read_from_file(self, path):
        path = Path(path)
        journal = SSHLogJournal()
        if not path.exists():
            logging.warning(f"Couldn't open {path}")
            return None
        else:
            try:
                with open(path) as f:
                    for line in f:
                        try:
                            journal.append(line, self.creator)
                        except ValueError:
                            logging.warning(f"Couldn't parse: {line}")
            except Exception:
                raise ValueError("Can't parse file")

        return journal

    def is_correct_extension(self, path):
        return Path(path).suffix == ".log"

    def can_be_opened(self, path):
        path = Path(path)
        return path.is_file() and access(path, R_OK)