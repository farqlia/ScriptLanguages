import fileinput
import os
import pathlib
import shutil
from subprocess import run, Popen, PIPE
import csv
import json

import pytest


def test_pass():
    pass

def test_file_path():
    assert r"C:\Users\julia\PycharmProjects\ScriptLanguages\lectures\filesystems\test\test_manipulate_fikes.py" == __file__

# PurePath : doesn't have OS operations; can be used to manipulate Windows paths on Unix systems
# Path : OS functionality

def test_path_creation():

    path = pathlib.Path(r"C:\Users\julia\PycharmProjects\ScriptLanguages\lectures\filesystems\test")
    assert path.parent == pathlib.Path(r"C:\Users\julia\PycharmProjects\ScriptLanguages\lectures\filesystems")
    assert path.parents[0] == pathlib.Path(r"C:\Users\julia\PycharmProjects\ScriptLanguages\lectures\filesystems")


def test_join_path():

    path = pathlib.Path(r"C:\Users\julia\PycharmProjects\ScriptLanguages\lectures")
    path = path.joinpath("filesystems", "test")
    assert path == pathlib.Path(r"C:\Users\julia\PycharmProjects\ScriptLanguages\lectures\filesystems\test")


def test_glob():

    # rglob - recursive glob
    path = pathlib.Path(r"C:\Users\julia\PycharmProjects\ScriptLanguages\lectures\filesystems")
    found_dirs = list(path.rglob("dir*"))
    assert found_dirs[0].is_dir()
    assert found_dirs[1].is_dir()


def test_other_functions():
    path = pathlib.Path(r"C:\Users\julia\PycharmProjects\ScriptLanguages\lectures\filesystems\test")
    # Useful for file size
    print(path.stat())
    print(path.home())


def walktree(top, callback):
    # Normally it doesnt go recursively
    for path in top.iterdir():
        if path.is_dir():
            walktree(path, callback)
        elif path.is_file():
            callback(path)
        else:
            print(f"Skipping {path}")


def visitfile(file):
    print('visiting', file)


def visit_dir(root, directory):
    print(f"[d] visiting {directory} in {root}")


def visit_file(root, file):
    print(f"[f] visiting {file} in {root}")


def traverse(directory, dir_callback, file_callback):
    for root, dirs, files in os.walk(directory):
        for direc in dirs:
            dir_callback(root, direc)
        for file in files:
            file_callback(root, file)


def test_walktree():
    path = pathlib.Path(r"C:\Users\julia\PycharmProjects\ScriptLanguages\lectures\filesystems")
    walktree(path, visitfile)


def test_walktree_2():
    path = pathlib.Path(r"C:\Users\julia\PycharmProjects\ScriptLanguages\lectures\filesystems")
    traverse(path, visit_dir, visit_file)


@pytest.fixture()
def mock_file(tmp_path):
    file = tmp_path.joinpath("file.txt")
    file.write_text("This is sparta")
    return file

@pytest.fixture()
def mock_file_opened(mock_file):

    f = open(pathlib.Path(mock_file))

    yield f

    f.close()



def test_reading_file(mock_file_opened):

    assert "This is sparta" == mock_file_opened.readline()
    assert "r" == mock_file_opened.mode


def test_binary():
    print((b"Hello").encode("utf-8"))
    name = b"\x4d\x61\x72\x63\x69\x6e"
    assert name == b"Marcin"


def test_code_bytes():
    assert b'\x7E'.decode('utf-8') == '~'
    assert '~'.encode('utf-8') == b'\x7E'
    assert 'ą'.encode('utf-8') == b'\xc4\x85'


def test_context_manager(mock_file):

    with open(mock_file) as f:
        for line in f:
            print(line)

    assert f.mode == "r"
    assert f.closed


@pytest.fixture()
def mock_file_2(tmp_path):
    file = tmp_path.joinpath("file2.txt")
    file.write_text("This is barcelona")
    return file


def test_many_inputs(mock_file, mock_file_2):

    data = ""
    with fileinput.input(files=(mock_file, mock_file_2), encoding='utf-8') as f:
        for line in f:
            data += line + "\n"

    data = data.rstrip()
    assert data == "This is sparta\nThis is barcelona"


# shutil : can use most linux files commands
def test_shutil(mock_file, mock_file_2):

    f = open(mock_file, 'r')
    f1 = open(mock_file_2, 'w')

    shutil.copyfileobj(f, f1)

    f.close()
    f1.close()


def test_shutil_more():
    assert r"C:\Users\julia\anaconda3\envs\ScriptLanguages\python.EXE" == shutil.which("python")


def test_use_environ():
    for env in os.environ: print(f"{env} = {os.environ[env]}")
    assert os.pathsep == ';'


def test_run_process():

    p = run(["python", "-c", "print('Hello World')"])
    assert p.returncode == 0

# Why not working
def test_piped_process():

    process = Popen(["tail", "-n", "2"], stdin=PIPE, stdout=PIPE, text=True)
    for i in range(10):
        _ = process.stdin.write(f"{i}th line \n")

    process.stdin.close()
    assert "8th line \n 9th line \n" == process.stdin.readlines()


@pytest.fixture()
def mock_csv(tmp_path):

    file = tmp_path.joinpath("data.csv")
    file.write_text("col1,col2,col3\n1,2,3")
    return file


def test_read_dict_csv(mock_csv):
    with open(mock_csv, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            assert ('1', '2', '3') == (row['col1'], row['col2'], row['col3'])


@pytest.fixture()
def mock_json():
    data = {"name": "Jan", "Nazwisko": "Kowalski"}
    json_data = json.dumps(data)
    return json_data


def test_read_json(mock_json):
    assert '{"name": "Jan", "Nazwisko": "Kowalski"}' == mock_json


def mock_json_file(tmp_path, mock_json):
    file = tmp_path.joinpath("data.json")
    file.write_text(mock_json)
    return file

@pytest.fixture()
def test_write_json(mock_json_file):
    with open(mock_json_file, 'rt') as json_data:
        data = json.loads(json_data.read())

    assert data == {"name": "Jan", "Nazwisko": "Kowalski"}