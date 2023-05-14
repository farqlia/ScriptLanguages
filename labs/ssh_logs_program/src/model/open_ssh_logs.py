from os import getcwd
from pathlib import Path
from subprocess import run

if __name__ == "__main__":
    ssh_logs = Path(getcwd()).parent.joinpath('data', 'SSH.tar.gz')
    print(ssh_logs)
    dest_shh_logs = Path(getcwd()).parent.joinpath('data')

    process = run(['tar', '-zxvf', ssh_logs, '-C', dest_shh_logs],
                  text=True)