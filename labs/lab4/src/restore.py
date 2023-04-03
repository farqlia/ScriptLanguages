import os
from pathlib import Path

import labs.lab4.src.lab4_4 as lab4
from labs.lab4.src.lab4_3 import get_dir_path_from_args


def to_restore_dir():
    _dir = get_dir_path_from_args()
    if not _dir:
        _dir = Path(os.getcwd())
    else:
        _dir = Path(_dir)
        _dir = _dir if _dir.exists() else Path(os.getcwd())
    return _dir


if __name__ == "__main__":

    lab4.print_formatted_archive_history()

    i = int(input("Enter index of archive to restore: "))

    tar_restore = lab4.TarRestore(to_restore_dir())
    tar_restore.restore(i)

