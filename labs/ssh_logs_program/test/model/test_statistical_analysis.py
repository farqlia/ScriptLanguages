import math

import labs.ssh_logs_program.src.model.statistical_analysis as statistical_analysis
import labs.ssh_logs_program.src.model.ssh_logs_prepare as ssh_logs_prepare
import labs.ssh_logs_program.src.model.regex_ssh_utilis as regex_ssh_analysis

import pytest
from pathlib import Path

parser = ssh_logs_prepare.Parser()

@pytest.fixture
def one_user_entries():
    entries = []
    with open(Path.cwd().parent.joinpath('data', 'one_user.log')) as f:
        for line in f:
            entries.append(parser.parse_entry(line))
    return entries


@pytest.fixture
def test_entries():
    entries = ["Dec 10 11:44:56 LabSZ sshd[28321]: Connection closed by 1.237.174.253 [preauth]",
               "Dec 10 11:44:56 LabSZ sshd[28325]: pam_unix(sshd:auth): authentication failure; logname= uid=0 euid=0 tty=ssh ruser= rhost=183.62.140.253  user=root",
               "Dec 10 11:44:58 LabSZ sshd[28525]: Failed password for root from 183.62.140.253 port 40480 ssh2",
               "Dec 10 11:48:00 LabSZ sshd[28523]: pam_unix(sshd:auth): authentication failure; logname= uid=0 euid=0 tty=ssh ruser= rhost=180.101.249.16  user=root",
               "Dec 10 11:48:02 LabSZ sshd[28525]: Failed password for root from 180.101.249.16 port 53496 ssh2",
               "Dec 10 11:48:13 LabSZ sshd[28325]: Disconnecting: Too many authentication failures for root [preauth]",
               "Dec 10 11:48:13 LabSZ sshd[28525]: PAM 5 more authentication failures; logname= uid=0 euid=0 tty=ssh ruser= rhost=180.101.249.16  user=root",
               "Dec 10 11:48:02 LabSZ sshd[28525]: Received disconnect from 183.62.140.253: 11: Bye Bye [preauth]"]
    return list(map(parser.parse_entry, entries))

@pytest.fixture
def test_entries_2():
    entries = ["Dec 10 08:33:24 LabSZ sshd[24385]: pam_unix(sshd:auth): authentication failure; logname= uid=0 euid=0 tty=ssh ruser= rhost=103.207.39.212",
                "Dec 10 08:33:26 LabSZ sshd[24385]: Received disconnect from 103.207.39.212: 11: Closed due to user request. [preauth]",
                'Dec 10 08:33:27 LabSZ sshd[24387]: pam_unix(sshd:auth): authentication failure; logname= uid=0 euid=0 tty=ssh ruser= rhost=103.207.39.212  user=uucp',
                "Dec 10 08:33:29 LabSZ sshd[24389]: Invalid user admin from 103.207.39.212",
                "Dec 10 08:33:29 LabSZ sshd[24389]: input_userauth_request: invalid user admin [preauth]",
                "Dec 10 08:33:31 LabSZ sshd[24389]: Failed password for invalid user admin from 103.207.39.212 port 58447 ssh2",
                ]
    return list(map(parser.parse_entry, entries))


def test_random_user(one_user_entries):
    print(statistical_analysis.get_random_user(one_user_entries))


def test_random_logs(one_user_entries):
    print(statistical_analysis.get_n_random_entries(one_user_entries, 3))


def test_global_connection_times(one_user_entries):
    mean, std = statistical_analysis.global_connection_time(one_user_entries)
    assert mean == (4 / 3)
    assert std == math.sqrt(((2 - mean) ** 2 + (2 - mean) ** 2) / 2)


def test_user_connection_times_2(test_entries_2):
    connection_times = statistical_analysis.user_connection_time(test_entries_2)
    print(connection_times)
    assert connection_times['request'][1] == 0


def test_user_connection_times_with_different_years():

    with open(r'C:\Users\julia\PycharmProjects\ScriptLanguages\labs\lab5\data\SSH_sample_logs.log') as f:

        specific_user = [parser.parse_entry(row) for row in f]

        print()
        for row in specific_user:
            print(row)

        print(statistical_analysis.compute_user_connection_times(specific_user))
        print(statistical_analysis.user_connection_time(specific_user))
        print(statistical_analysis.global_connection_time(specific_user))


def test_frequency(test_entries_2):
    most, least = statistical_analysis.get_most_and_least_active(test_entries_2)
    assert most == 'admin'
    assert least == 'uucp'