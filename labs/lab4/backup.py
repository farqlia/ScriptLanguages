from pathlib import Path

import labs.lab4.lab4_4 as lab4
from labs.lab4.lab4_3 import get_dir_path

if __name__ == "__main__":

    _dir = get_dir_path()

    if _dir:
        tar_archive = lab4.TarArchive(Path(_dir))
        tar_archive.archive()



