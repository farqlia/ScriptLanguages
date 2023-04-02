import abc
import os
from pathlib import Path
import csv
from subprocess import run

import datetime

FORMAT = "%Y-%m-%d-%H-%M-%S"

FIELDNAMES = ['Date', 'Full Directory Path', 'Archive Name']


def get_user_home():
    return os.path.expanduser("~" + os.environ['USERNAME'])


def get_backups_directory():
    backup_dir = os.environ.get('BACKUPS_DIR', os.path.join(get_user_home(), ".backups"))
    backup_dir_path = Path(backup_dir)
    # Creates the backup directory and all subdirectories if needed
    backup_dir_path.mkdir(parents=True, exist_ok=True)
    return backup_dir_path


def get_archive_history_path():
    return Path(get_backups_directory()) / "archive_history.csv"


# This must be called
def create_archive_history_file():

    if not get_archive_history_path().exists():
        with open(get_archive_history_path(), mode='w', newline='') as f:
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

    def create_archive_name(self):
        return get_backups_directory() / f"{self.creation_date}-{self.dir_path.stem}.{self.ext}"

    def write_to_archive_history(self):
        with open(get_archive_history_path(), mode='a', newline='') as f:
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

    def remove_from_archive_history(self, index):

        archive_history_path_temp = get_backups_directory() / "archive_history_temp.csv"

        with open(get_archive_history_path(), newline='') as f_read, \
                open(archive_history_path_temp, mode='w', newline='') as f_write:
            reader = csv.DictReader(f_read, fieldnames=FIELDNAMES)
            writer = csv.DictWriter(f_write, fieldnames=FIELDNAMES)

            next(reader)
            writer.writeheader()

            n_records = 0
            for row in reader:
                if n_records == index:
                    self.archive_path = get_backups_directory() / (row['Archive Name'] + '.' + self.ext)
                else:
                    writer.writerow(row)
                n_records += 1

        archive_history_path_temp.replace(get_archive_history_path())

        return self.archive_path


class TarArchive(Archive):

    def __init__(self, dir_path):
        super().__init__(dir_path=dir_path, ext='tar')

    def archive(self):
        self.archive_path = Path(self.create_archive_name())
        process = run(['tar', '-cvzf', self.archive_path, self.dir_path],
                      text=True)
        self.write_to_archive_history()
        return process.returncode == 0


class TarRestore(Restore):

    def __init__(self, dir_path):
        super().__init__(dir_path, 'tar')

    def restore(self, index):
        self.archive_path = get_backups_directory() / self.remove_from_archive_history(index)
        process = run(['tar', '-zxvf', self.archive_path, '-C', self.dir_path],
                      text=True)
        # os.remove(self.archive_path)
        return process.returncode == 0


def open_archive_history(reverse=False):

    backups = []
    with open(get_archive_history_path(), newline='') as f:
        reader = csv.DictReader(f, fieldnames=FIELDNAMES)
        next(reader)
        for row in reader:
            backups.append(row)

    backups = list(zip(range(len(backups)), backups))
    return backups if not reverse else backups[::-1]


def print_formatted_archive_history():

    history = open_archive_history(reverse=True)
    for (i, row) in history:
        print(f"[{i}], {row}")


