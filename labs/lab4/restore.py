import os
from pathlib import Path

import labs.lab4.lab4_4 as lab4
from labs.lab4.lab4_3 import get_dir_path

if __name__ == "__main__":

    _dir = get_dir_path()
    _dir = Path(os.getcwd()) if not _dir else _dir

    lab4.print_formatted_archive_history()

    i = int(input("Enter index"))

    tar_restore = lab4.TarRestore(_dir)
    tar_restore.restore(i)

