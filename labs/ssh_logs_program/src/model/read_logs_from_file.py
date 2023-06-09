from os import access, R_OK
from pathlib import Path
from labs.ssh_logs_program.src.model.ssh_log_journal import LogJournal, SSHLogJournal
from labs.ssh_logs_program.src.model.log_factory import OtherCreator
import logging
import abc
from typing import Union, Optional


class LogHandler(abc.ABC):

    def read_from_file(self, path: Union[Path, str]) -> Optional[LogJournal]:
        return None

    def is_correct_extension(self, path: Union[Path, str]) -> bool:
        return False

    def can_be_opened(self, path: Union[Path, str]) -> bool:
        return False


class SSHLogsHandler(LogHandler):

    def __init__(self):
        self.creator = OtherCreator()

    def read_from_file(self, path: Union[Path, str]) -> Optional[LogJournal]:
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

    def is_correct_extension(self, path: Union[Path, str]) -> bool:
        return Path(path).suffix == ".log"

    def can_be_opened(self, path: Union[Path, str]) -> bool:
        path = Path(path)
        return path.is_file() and access(path, R_OK)