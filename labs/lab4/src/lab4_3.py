import json
import os
import sys
from pathlib import Path
from labs.lab4.src.lab4_1 import any_argument
import subprocess
import logging

FILE_PATH = r"C:\Users\julia\PycharmProjects\ScriptLanguages\labs\lab4\src\analyze_file.py"


def get_dir_path_from_args():
    _dir = ""
    if any_argument():
        _dir = Path(sys.argv[1])
        _dir = _dir if _dir.is_dir() else ""
    return _dir


def run_analysis(filepath):
    process = subprocess.run(["python", FILE_PATH],
                             stdout=subprocess.PIPE,
                             encoding='ascii',
                             input=filepath)

    output = "" if process.returncode else process.stdout.strip()
    return output


def traverse_files(directory, file_callback):
    for dir_path, _, files in os.walk(directory):
        for file in files:
            file_callback(os.path.join(dir_path, file))


def run_files_analyses(dir_path):

    analyses = []

    def add_to_list(file):
        output = run_analysis(file)
        if output:
            analyses.append(json.loads(output))

    traverse_files(dir_path, add_to_list)

    return analyses


def print_results(analyses):

    for analysis in analyses:
        print(json.dumps(analysis, indent=4))


if __name__ == "__main__":

    logging.basicConfig(filename=f"{Path(__file__).stem}_logging.txt",
                        encoding='utf-8', level=logging.DEBUG)

    _dir = get_dir_path_from_args()

    if _dir:
        print_results(run_files_analyses(_dir))
    else:
        logging.error(f"Not a directory: {_dir}")

