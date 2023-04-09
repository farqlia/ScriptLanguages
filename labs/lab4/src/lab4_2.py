import os
import pathlib
import shutil
import stat
import sys


def get_path_listing():
    path = os.environ['PATH']
    return [pathlib.Path(elem) for elem in path.split(os.pathsep) if len(elem) > 0]


def get_path_contents(include_execs=False):
    dirs = get_path_listing()
    if include_execs:
        dirs = {_dir: list(map(lambda p: p.stem, filter(lambda f: os.stat(f).st_mode & stat.S_IXUSR, list(_dir.iterdir()))))
                for _dir in dirs if _dir.is_dir()}
    return dirs


def print_exe():
    return len(sys.argv) > 1 and sys.argv[1].lower().startswith('t')


if __name__ == "__main__":

    if print_exe():
        for k, v in get_path_contents(True).items():
            print(f"[d] {k}")
            print(f"{v}")

    else:
        for d in get_path_contents(False):
            print(f"{d}")