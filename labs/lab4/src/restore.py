import os
from pathlib import Path

import labs.lab4.src.lab4_4 as lab4
from labs.lab4.src.lab4_3 import get_dir_path_from_args

if __name__ == "__main__":

    _dir = get_dir_path_from_args()
    _dir = Path(os.getcwd()) if not _dir else _dir

    lab4.print_formatted_archive_history()

    i = int(input("Enter index"))

    tar_restore = lab4.TarRestore(_dir)
    tar_restore.restore(i)

