import os
from pathlib import Path
import csv

import labs.lab4.lab4_3 as lab4_3
import datetime

FORMAT = "%Y_%m_%d_%H_%M_%S"

FIELDNAMES = ['Date', 'Full Directory Path', 'Archive Name']


def get_user_home():
    return os.path.expanduser("~" + os.environ['USERNAME'])


def get_backups_directory():
    backup_dir = os.environ.get('BACKUPS_DIR', os.path.join(get_user_home(), "backups"))
    backup_dir_path = Path(backup_dir)
    # Creates the backup directory and all subdirectories if needed
    backup_dir_path.mkdir(parents=True, exist_ok=True)
    return backup_dir_path

class Archive:

    def __init__(self, dirname, ext):
        self.creation_date = datetime.datetime.now().strftime(FORMAT)
        self.dirname = dirname
        self.ext = ext

    def create_archive_name(self, dirname, ext):
        return f"{self.creation_date}-{dirname}.{ext}"

    def archive(self):
        self.archive_path = Path()
        pass

    def update_archive_history(self):
        archive_history_file = Path(get_backups_directory() / "archive_history.csv")
        with open(archive_history_file, mode='a', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=FIELDNAMES)
            writer.writerow({'Date': self.creation_date,
                             'Full Directory Path': self.dirname,
                             'Archive Name': self.archive_path.stem})
















