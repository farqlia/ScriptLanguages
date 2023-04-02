from pathlib import Path

import labs.lab4.src.lab4_4a as lab4
from labs.lab4.src.lab4_3 import get_dir_path_from_args

if __name__ == "__main__":

    lab4.create_archive_history_file()

    _dir = get_dir_path_from_args()

    if _dir:
        tar_archive = lab4.TarArchive(Path(_dir))
        tar_archive.archive()



