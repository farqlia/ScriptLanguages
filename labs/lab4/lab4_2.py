import os
import pathlib
import stat
import sys


def get_path_directories():
    path = os.environ['PATH']
    return list(filter(lambda s: len(s.strip()) > 0, path.split(os.pathsep)))


def is_exe_windows(filepath):
    return filepath.endswith(".exe")


def is_exe_posix(filepath):
    # Can also do stat.S_IXGRP, stat.S_IXUSR, stat.S_IXOTH for
    # execute permissions for others
    return os.stat(filepath).st_mode & stat.S_IXUSR
    # return os.access(filepath, os.X_OK)


def is_executable():
    print("invoked")
    return is_exe_windows if os.name == 'nt' else is_exe_posix


def get_path_contents(include_execs=False):
    dirs = get_path_directories()
    if include_execs:
        is_exe = is_executable()
        dirs = {_dir: list(filter(is_exe, os.listdir(_dir))) for _dir in dirs if pathlib.Path(_dir).is_dir()}
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