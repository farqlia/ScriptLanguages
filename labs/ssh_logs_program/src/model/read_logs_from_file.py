from pathlib import Path
from labs.ssh_logs_program.src.model.ssh_log_journal import LogJournal, SSHLogJournal
from labs.ssh_logs_program.src.model.log_factory import OtherCreator
import logging
import abc


class LogHandler(abc.ABC):

    def read_from_file(self, path: str) -> LogJournal:
        pass


class SSHLogsHandler(LogHandler):

    def __init__(self):
        self.creator = OtherCreator()

    def read_from_file(self, path: str):
        path = Path(path)
        journal = SSHLogJournal()
        if not path.exists():
            logging.warning(f"Couldn't open {path}")
            return None
        else:
            with open(path) as f:
                for line in f:
                    try:
                        journal.append(line, self.creator)
                    except ValueError:
                        logging.warning(f"Couldn't parse: {line}")

        return journal
