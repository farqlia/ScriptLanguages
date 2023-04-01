import abc
import os
import shutil
from pathlib import Path
import csv
from subprocess import run

import labs.lab4.lab4_3 as lab4_3
import datetime

FORMAT = "%Y-%m-%d-%H-%M-%S"

FIELDNAMES = ['Date', 'Full Directory Path', 'Archive Name']


def get_user_home():
    return os.path.expanduser("~" + os.environ['USERNAME'])


def get_backups_directory():
    backup_dir = os.environ.get('BACKUPS_DIR', os.path.join(get_user_home(), "backups"))
    backup_dir_path = Path(backup_dir)
    # Creates the backup directory and all subdirectories if needed
    backup_dir_path.mkdir(parents=True, exist_ok=True)
    return backup_dir_path


archive_history_path = Path(get_backups_directory()) / "archive_history.csv"


# This must be called
def create_archive_history_file():

    if not archive_history_path.exists():
        with open(archive_history_path, mode='w', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=FIELDNAMES)
            writer.writeheader()


class Archive(abc.ABC):

    create_archive_history_file()

    @abc.abstractmethod
    def archive(self):
        pass

    # If unpack
    def __init__(self, dir_path, ext):
        self.creation_date = datetime.datetime.now().strftime(FORMAT)
        self.dir_path = dir_path
        self.archive_path = Path()
        self.ext = ext

    def validate(self):
        return self.dir_path.is_dir()

    def create_archive_name(self):
        return get_backups_directory() / f"{self.creation_date}-{self.dir_path.stem}.{self.ext}"

    def write_to_archive_history(self):
        with open(archive_history_path, mode='a', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=FIELDNAMES)
            writer.writerow({'Date': self.creation_date,
                             'Full Directory Path': str(self.dir_path),
                             'Archive Name': self.archive_path.stem})


class Restore(abc.ABC):

    @abc.abstractmethod
    def restore(self, index):
        pass

    def __init__(self, dir_path, ext):
        self.dir_path = dir_path
        self.archive_path = Path()
        self.ext = ext

    def validate(self):
        return self.dir_path.is_dir()

    def remove_from_archive_history(self, index):

        archive_history_path_temp = get_backups_directory() / "archive_history_temp.csv"

        with open(archive_history_path, newline='') as f_read, \
                open(archive_history_path_temp, mode='w', newline='') as f_write:
            reader = csv.DictReader(f_read, fieldnames=FIELDNAMES)
            writer = csv.DictWriter(f_write, fieldnames=FIELDNAMES)
            # We skip the header
            n_records = -1
            for row in reader:
                if n_records == index:
                    self.archive_path = get_backups_directory() / (row['Archive Name'] + '.' + self.ext)
                else:
                    writer.writerow(row)
                n_records += 1

        archive_history_path_temp.replace(archive_history_path)

        return self.archive_path


class TarArchive(Archive):

    def __init__(self, dir_path):
        super().__init__(dir_path=dir_path, ext='tar')

    def archive(self):
        if self.validate():
            self.archive_path = Path(self.create_archive_name())
            process = run(['tar', '-cvzf', self.archive_path, self.dir_path],
                          text=True)
            self.write_to_archive_history()
            return process.returncode == 0
        return False


class TarRestore(Restore):

    def __init__(self, dir_path):
        super().__init__(dir_path, 'tar')

    def restore(self, index):
        if self.validate():
            self.archive_path = get_backups_directory() / self.remove_from_archive_history(index)
            process = run(['tar', '-zxvf', self.archive_path, '-C', self.dir_path],
                          text=True)
            os.remove(self.archive_path)
            return process.returncode == 0
        return False






