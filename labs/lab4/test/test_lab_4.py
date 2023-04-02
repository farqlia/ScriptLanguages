import csv
import json
import os
import shutil
import stat
from pathlib import Path

import pytest

from labs.lab4.src.lab4_2 import get_path_contents
import labs.lab4.src.lab4_2 as lab_2
import labs.lab4.src.lab4_3 as lab_3
import labs.lab4.src.lab4_4 as lab_4a


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

    def test_if_posix_exe(self):

        # Shutil checks whether a command prompted in cmd with a given name
        # would run - if yes

        executable = Path(r"C:\Users\julia\anaconda3\bin\nvlink.exe")
        print(os.stat(executable).st_mode & stat.S_IXUSR)
        print(os.stat(executable).st_mode & stat.S_IXGRP)
        print(os.stat(executable).st_mode & stat.S_IXOTH)
        print(stat.filemode(os.stat(executable).st_mode))

        assert shutil.which(executable.stem)

        executable = Path(r"C:\Users\julia\anaconda3\bin\nvcc.exe")
        print(os.stat(executable).st_mode & stat.S_IXUSR)
        print(os.stat(executable).st_mode & stat.S_IXGRP)
        print(os.stat(executable).st_mode & stat.S_IXOTH)
        print(stat.filemode(os.stat(executable).st_mode))

        assert shutil.which(executable.stem)

        not_executable = Path(r"C:\Users\julia\anaconda3\README")
        print(os.stat(not_executable).st_mode & stat.S_IXUSR)
        print(os.stat(not_executable).st_mode & stat.S_IXGRP)
        print(os.stat(not_executable).st_mode & stat.S_IXOTH)
        print(stat.filemode(os.stat(not_executable).st_mode))

        assert not shutil.which(not_executable.stem)

    def test_get_path_folders_and_execs(self):
        dirs_and_execs = get_path_contents(include_execs=True)
        assert dirs_and_execs[Path("C:\\Users\\julia\\anaconda3\\envs\\ScriptLanguages")] == [
            'python',
            'pythonw'
        ]

    def test_get_path_folders(self):
        dirs = get_path_contents(False)
        for dir in dirs:
            print(dir)

    def filter_with_shutil(self, dir_path):
        # for file in os.listdir(dir_path):
        #    print(file, " ", shutil.which(file.stem))
        return list(map(lambda f: Path(f).stem, filter(lambda f: bool(shutil.which(f)), os.listdir(dir_path))))

    def test_filter(self):
        filtered = self.filter_with_shutil(Path("C:\Windows\system32"))
        way = lab_2.get_path_contents(include_execs=True)

        assert set(way[Path('C:\Windows\system32')]) == set(filtered)


    def test_mock_print_path_folders_and_execs(self, mocker):
        mocker.patch('labs.lab4.lab4_2.get_path_directories',
                          return_value=[r"C:\Users\julia\PycharmProjects\ScriptLanguages\labs"])
        print(get_path_contents(include_execs=True))


    def test_mock_print_path_folders(self, mocker):
        mocker.patch('labs.lab4.lab4_2.get_path_directories',
                           return_value=[r"C:\Users\julia\PycharmProjects\ScriptLanguages\labs\lab4"])
        print(get_path_contents(include_execs=False))


@pytest.fixture
def dir_to_analyze(tmp_path):
    _dir = tmp_path / "to_analyze"
    _dir.mkdir()
    file = _dir / "file1.txt"
    file.write_text("World is big\nPython is great")
    file = _dir / "file2.txt"
    file.write_text("Mamma mia\nItaliana")
    subdir = _dir / "sub_to_analyze"
    subdir.mkdir()
    file = subdir / "file3.txt"
    file.write_text("To be\nOr Not\nto be")
    return _dir


class TestAnalyseFile:

    @pytest.fixture
    def example_file(self, tmp_path):
        file = tmp_path / "words.txt"
        file.write_text("World is big\nPython is great")
        return file

    def test_run_analysis(self, example_file):
        print(str(example_file))
        output = lab_3.run_analysis(str(example_file))
        json_output = json.loads(output)
        expected = {'filepath': str(example_file),
        'n_of_lines': 2,
        'max_char': 'i',
        'max_word': 'is',
        'n_words': 6,
        'n_chars': 23}
        assert json_output == expected

    def test_run_nonexisting_analysis(self):
        not_existing = "\\"
        output = lab_3.run_analysis(not_existing)
        assert output == ""

    def test_traverse_files(self):
        files = []
        func = lambda f: files.append(Path(f).name)
        _dir = r"C:\Users\julia\PycharmProjects\ScriptLanguages\labs\lab4\input_data"
        lab_3.traverse_files(_dir, func)
        assert files == ['supernova.txt', 'zenofpython.txt', 'irish_airman_death']


    # TODO : write this test
    def test_run_files_analyses(self, dir_to_analyze):

        expected = [{'filepath': str(dir_to_analyze / 'file1.txt'), 'n_of_lines': 2, 'max_char': 'i', 'max_word': 'is', 'n_words': 6, 'n_chars': 23},
                    {'filepath': str(dir_to_analyze / 'file2.txt'), 'n_of_lines': 2, 'max_char': 'a', 'max_word': 'Mamma', 'n_words': 3, 'n_chars': 16},
                    {'filepath': str(dir_to_analyze / 'sub_to_analyze\\file3.txt'), 'n_of_lines': 3, 'max_char': 'o', 'max_word': 'be', 'n_words': 6, 'n_chars': 13}]

        actual = lab_3.run_files_analyses(dir_to_analyze)

        assert actual == expected


class TestCreateArchive:

    def test_get_user_home(self):
        assert "julia" == os.environ['USERNAME']
        assert r"C:\Users\julia" == os.path.expanduser("~" + os.environ['USERNAME'])

    def test_create_tar_archive_with_default_backup_dir(self, dir_to_analyze):
        assert dir_to_analyze.is_dir()
        tar_archive = lab_4a.TarArchive(dir_to_analyze)
        assert tar_archive.archive()
        assert tar_archive.archive_path.exists()

    def test_unsuccessful_archive(self):
        non_existing_dir = Path(r"C:\julia\not_existing")
        assert not non_existing_dir.exists()
        tar_archive = lab_4a.TarArchive(non_existing_dir)
        assert not tar_archive.archive()
        assert not tar_archive.archive_path.exists()

    def test_create_tar_archive_with_defined_backup_dir(self, dir_to_analyze, tmp_path):

        backup_dir = tmp_path / "backup"
        os.environ['BACKUPS_DIR'] = str(backup_dir)

        assert not backup_dir.exists()
        assert dir_to_analyze.is_dir()
        assert lab_4a.get_backups_directory() == backup_dir

        tar_archive = lab_4a.TarArchive(dir_to_analyze)
        assert tar_archive.archive()

        _subdir = dir_to_analyze / "sub_to_analyze"

        tar_archive = lab_4a.TarArchive(_subdir)
        assert tar_archive.archive()

        with open(lab_4a.get_archive_history_path(), newline='') as f:
            reader = csv.DictReader(f, lab_4a.FIELDNAMES)
            rows = list(reader)

        assert rows[0]['Full Directory Path'].endswith('to_analyze')
        assert rows[1]['Full Directory Path'].endswith('\\to_analyze\\sub_to_analyze')


class TestTarRestore:

    @pytest.fixture
    def archive_test(self, dir_to_analyze, tmp_path):
        backup_dir = tmp_path / "backup_test"
        os.environ['BACKUPS_DIR'] = str(backup_dir)

        tar_archive = lab_4a.TarArchive(dir_to_analyze)
        tar_archive._archive()
        yield tar_archive.archive_path

        shutil.rmtree(backup_dir)

    def test_restore_archive(self, archive_test, tmp_path):

        restore_to = tmp_path / 'data'
        restore_to.mkdir()

        restored_archive = lab_4a.TarRestore(restore_to)
        restored_archive.restore(0)

        print(restored_archive.archive_path)
        print(restored_archive.dir_path)

        assert not restored_archive.archive_path.exists()
        assert (restore_to / "to_analyze").exists()

    def test_remove_from_archive_history(self, archive_test, tmp_path):

        restore_to = tmp_path / 'data'
        restore_to.mkdir()

        with open(lab_4a.get_archive_history_path(), newline='') as f:
            reader = csv.DictReader(f, lab_4a.FIELDNAMES)
            for row in reader:
                print(json.dumps(row, indent=4))

        restored_archive = lab_4a.TarRestore(restore_to)
        restored_archive.remove_from_archive_history(0)

        print("----- AFTER RESTORING ----------")

        with open(lab_4a.get_archive_history_path(), newline='') as f:
            reader = csv.DictReader(f, lab_4a.FIELDNAMES)
            for row in reader:
                print(json.dumps(row, indent=4))

    def test_open_archive_history(self):
        lab_4a.print_formatted_archive_history()





