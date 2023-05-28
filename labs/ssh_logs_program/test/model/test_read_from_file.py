import pytest
from labs.ssh_logs_program.src.model import read_logs_from_file
from labs.ssh_logs_program.src.model import logging_configure

logging_configure.configure_logging()


@pytest.fixture()
def file(tmp_path):
    f = tmp_path / "file.logs"
    f.write_text('''Dec 10 11:40:36 LabSZ sshd[27952]: Failed password for invalid user webadmin from 183.62.140.253 port 51013 ssh2\nDec 10 11:40:36 LabSZ sshd[27952]: Received disconnect from 183.62.140.253: 11: Bye Bye [preauth]
    ''')
    return f


def test_read_successfully_from_file(file):
    logs = read_logs_from_file.SSHLogsHandler().read_from_file(file)
    assert len(logs) == 2


def test_read_unsuccessfully_from_file():
    logs = read_logs_from_file.SSHLogsHandler().read_from_file("data/")
    assert logs is None
