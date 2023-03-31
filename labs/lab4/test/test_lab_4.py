import os
import sys
from pathlib import Path
import pytest_mock

from labs.lab4.lab4_2 import get_path_contents


class TestPrintExecutable:

    def test_platform(self):
        # for unix, macos it will be posix
        assert os.name == 'nt'

    def test_print_os_separator(self):
        print(os.pathsep)

    def test_if_executable(self):
        not_executable = Path(r"C:\Users\julia\anaconda3\bin\nvcc.profile")
        executable = Path(r"C:\Users\julia\anaconda3\bin\nvlink.exe")

        assert not os.access(not_executable, os.X_OK)
        assert os.access(executable, os.X_OK)

    def test_get_path_folders_and_execs(self):
        dirs_and_execs = get_path_contents(include_execs=True)

        assert dirs_and_execs["C:\\Users\\julia\\anaconda3\\envs\\ScriptLanguages"] == ['python.exe', 'pythonw.exe']

    def test_get_path_folders(self):
        dirs = get_path_contents(False)
        for dir in dirs:
            print(dir)

    def test_mock_print_path_folders_and_files(self, mocker):
        mocker.patch('labs.lab4.lab4_2.is_executable',
                          return_value=True)
        print(get_path_contents(include_execs=True))

    def test_mock_print_path_folders_and_execs(self, mocker):
        mocker.patch('labs.lab4.lab4_2.get_path_directories',
                          return_value=[r"C:\Users\julia\PycharmProjects\ScriptLanguages\labs"])
        print(get_path_contents(include_execs=True))

    def test_mock_print_path_folders(self, mocker):
        mocker.patch('labs.lab4.lab4_2.get_path_directories',
                           return_value=[r"C:\Users\julia\PycharmProjects\ScriptLanguages\labs\lab4"])
        print(get_path_contents(include_execs=False))
