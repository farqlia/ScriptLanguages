import os
import stat
import sys
from pathlib import Path
import pytest_mock

from labs.lab4.lab4_2 import get_path_contents, is_exe_posix, is_executable, is_exe_windows


class TestPrintExecutable:

    def test_platform(self):
        # for unix, macos it will be posix
        assert os.name == 'nt'

    def test_print_os_separator(self):
        print(os.pathsep)

    def text_posix_exe(self):
        executable = Path(r"C:\Users\julia\anaconda3\bin\nvlink.exe")
        assert is_exe_posix(executable)


    def test_if_executable(self):
        not_executable = Path(r"C:\Users\julia\anaconda3\bin\nvcc.profile")
        executable = Path(r"C:\Users\julia\anaconda3\bin\nvlink.exe")

        assert not os.access(not_executable, os.X_OK)
        assert os.access(executable, os.X_OK)

    def test_if_posix_exe(self):
        executable = Path(r"C:\Users\julia\anaconda3\bin\nvlink.exe")
        print(os.stat(executable).st_mode & stat.S_IXUSR)
        print(os.stat(executable).st_mode & stat.S_IXGRP)
        print(os.stat(executable).st_mode & stat.S_IXOTH)
        print(stat.filemode(os.stat(executable).st_mode))

        not_executable = Path(r"C:\Users\julia\anaconda3\bin\nvcc.profile")
        print(os.stat(not_executable).st_mode & stat.S_IXUSR)
        print(os.stat(not_executable).st_mode & stat.S_IXGRP)
        print(os.stat(not_executable).st_mode & stat.S_IXOTH)
        print(stat.filemode(os.stat(not_executable).st_mode))

        assert is_exe_posix(executable)
        assert not is_exe_posix(not_executable)

    def test_get_path_folders_and_execs(self):
        dirs_and_execs = get_path_contents(include_execs=True)
        assert dirs_and_execs[Path("C:\\Users\\julia\\anaconda3\\envs\\ScriptLanguages")] == [
            Path('C:/Users/julia/anaconda3/envs/ScriptLanguages/python.exe'),
            Path('C:/Users/julia/anaconda3/envs/ScriptLanguages/pythonw.exe')
        ]

    def test_get_path_folders(self):
        dirs = get_path_contents(False)
        for dir in dirs:
            print(dir)

    def filter_exe_windows(self, dir_path):
        return list(filter(is_exe_windows, list(dir_path.iterdir()))) if Path(dir_path).is_dir() else []

    def filter_exe_posix(self, dir_path):
        return list(filter(is_exe_posix, list(dir_path.iterdir()))) if Path(dir_path).is_dir() else []

    def test_mock_print_path_folders_and_files(self):
        _dir = Path("C:\Windows\system32")
        content_windows = self.filter_exe_windows(_dir)
        print(content_windows)
        content_posix = self.filter_exe_posix(_dir)
        print(content_posix)


    def test_mock_print_path_folders_and_execs(self, mocker):
        mocker.patch('labs.lab4.lab4_2.get_path_directories',
                          return_value=[r"C:\Users\julia\PycharmProjects\ScriptLanguages\labs"])
        print(get_path_contents(include_execs=True))

    def test_mock_print_path_folders(self, mocker):
        mocker.patch('labs.lab4.lab4_2.get_path_directories',
                           return_value=[r"C:\Users\julia\PycharmProjects\ScriptLanguages\labs\lab4"])
        print(get_path_contents(include_execs=False))
