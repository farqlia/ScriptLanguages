from argparse import Namespace

import pandas as pd
from pathlib import Path
from os import getcwd
import pytest
import re
import labs.lab5.src.regex_ssh_utilis as analyze_ssh_logs
import labs.lab5.src.ssh_logs_prepare as ssh_logs_prepare
from collections import namedtuple
import time
import labs.lab5.src.app as app
import datetime

DATA_DIR = Path(getcwd()).parent.joinpath('data')
logs_link = ""

parser = ssh_logs_prepare.Parser()


def test_examine_log_structure():
    print()
    with open(DATA_DIR.joinpath('SSH_test_logs.log')) as f:
        for line in f:
            print(line)


def test_new_pattern():
    pattern = re.compile("(?P<date>\w+ \d{1,2} \d{2}:\d{2}:\d{2})")
    assert re.search(pattern, "Dec 10 06:55:46 LabSZ sshd[24200]").group() == "Dec 10 06:55:46"
    print(datetime.datetime.strptime("Dec 10 06:55:46", "%b %d %H:%M:%S"))


class TestParseEntry:
    @pytest.mark.parametrize("log,expected_groups",
                             [("Dec 10 06:55:46 LabSZ sshd[24200]: Invalid user webmaster from 173.234.31.186",
                               {'date': 'Dec 10 06:55:46',
                                'pid': '24200', 'message': 'Invalid user webmaster from 173.234.31.186'})])
    def test_pattern_for_parsing_logs(self, log, expected_groups):
        match = re.match(ssh_logs_prepare.Parser.PATTERN, log)
        assert all(expected_groups[k] == match.group(k) for k in expected_groups.keys())


    @pytest.mark.parametrize("entry,expected",
                             [("Dec 10 07:13:43 LabSZ sshd[24227]: Failed password for root from 5.36.59.76 port 42393 ssh2"
                               , {'date': datetime.datetime(year=2022, month=12, day=10, hour=7, minute=13, second=43),
                                  'host': 'LabSZ', 'pid': 24227,
                                  'message': 'Failed password for root from 5.36.59.76 port 42393 ssh2'}),
                              ])
    def test_convert_to_namedtuple(self, entry, expected):
        tuple_entry = parser.parse_entry(entry)
        assert tuple_entry.date == expected['date']
        assert tuple_entry.host == expected['host']
        assert tuple_entry.pid == expected['pid']
        assert tuple_entry.message == expected['message']
        assert len(tuple_entry) == len(expected)


class TestFilterPort:

    @pytest.mark.parametrize("entry,port",
                             [("Dec 10 07:13:43 LabSZ sshd[24227]: Failed password for root from 5.36.59.76 port 42393 ssh2", 42393),
                              ("Jan  5 09:48:18 LabSZ sshd[17431]: message repeated 5 times: [ Failed password for root from 59.63.188.30 port 60223 ssh2]", 60223),
                              ("Dec 10 23:13:45 LabSZ sshd[20073]: PAM 5 more authentication failures; logname= uid=0 euid=0 tty=ssh ruser= rhost=121.193.184.2 ", None),
                              ("Dec 10 23:24:19 LabSZ sshd[20079]: Invalid user chena from 52.80.34.196", None)])
    def test_cases(self, entry, port):
        assert analyze_ssh_logs.get_port(parser.parse_entry(entry)) == port


class TestErrorCause:

    instances_to_test = [
        "Dec 16 14:25:57 LabSZ sshd[27703]: error: Received disconnect from 103.79.141.133: 3: com.jcraft.jsch.JSchException: Auth fail [preauth]",
        "Dec 16 17:02:11 LabSZ sshd[29026]: error: connect_to 10.10.34.41 port 22: failed.",
        "Dec 17 05:17:45 LabSZ sshd[25192]: error: Received disconnect from 103.99.0.122: 14: No more user authentication methods available. [preauth]",
        "Jan  4 13:42:21 LabSZ sshd[32136]: error: Received disconnect from 212.83.176.1: 3: org.vngx.jsch.userauth.AuthCancelException: User authentication canceled by user [preauth]",
        "Jan  5 09:47:34 LabSZ sshd[17423]: error: Received disconnect from 195.154.45.62: 3: com.jcraft.jsch.JSchException: timeout in waiting for rekeying process. [preauth]"
    ]

    def test_pattern(self):
        example1 = "error: received disconnect from 103.79.141.133: 3: com.jcraft.jsch.JSchException: Auth fail [preauth]"
        print(analyze_ssh_logs.ERROR_CAUSE_PATTERN.search(example1).groups())
        example2 = "error: connect_to 10.10.34.41 port 22: failed."
        print(analyze_ssh_logs.ERROR_CAUSE_PATTERN.search(example2).groups())

    @pytest.mark.parametrize("entry,cause",
                             list(zip(instances_to_test,
                                      ["received disconnect: auth fail", "connection: failed",
                                       "received disconnect: no more user authentication methods available",
                                       "received disconnect: user authentication canceled by user",
                                       "received disconnect: timeout in waiting for rekeying process"])))
    def test_for_error_cause(self, entry, cause):
        assert analyze_ssh_logs.get_error_cause(parser.parse_entry(entry)) == cause


class TestGetIPv4Logs:

    @pytest.mark.parametrize("entry,expected_addresses",
                             [("Dec 10 06:55:48 LabSZ sshd[24200]: Connection closed by 173.234.31.186 [preauth]", ["173.234.31.186"]),
                              ("Dec 10 07:07:38 LabSZ sshd[24206]: Invalid user test9 from 52.80.34.196", ["52.80.34.196"]),
                              ("Dec 10 07:08:28 LabSZ sshd[24208]: pam_unix(sshd:auth): authentication failure; logname= uid=0 euid=0 tty=ssh ruser= rhost=173.234.31.186",
                               ["173.234.31.186"]),
                              ("Dec 10 07:13:31 LabSZ sshd[24227]: pam_unix(sshd:auth): authentication failure; logname= uid=0 euid=0 tty=ssh ruser= rhost=5.36.59.76.dynamic-dsl-ip.omantel.net.om  user=root",
                               ["5.36.59.76"]),
                              ("Dec 10 07:27:55 LabSZ sshd[24237]: Received disconnect from 112.95.230.3: 11: Bye Bye [preauth]",
                              ["112.95.230.3"]),
                              ("Dec 10 07:51:17 LabSZ sshd[24326]: reverse mapping checking getaddrinfo for 195-154-37-122.rev.poneytelecom.eu [195.154.37.122] failed - POSSIBLE BREAK-IN ATTEMPT!",
                               ["195.154.37.122"]),
                              ])
    def test_correct_cases(self, entry, expected_addresses):
        actual_addresses = analyze_ssh_logs.get_ipv4s_from_log(parser.parse_entry(entry))
        assert actual_addresses == expected_addresses


    @pytest.mark.parametrize("entry", ["Dec 10 07:55:55 LabSZ sshd[24331]: pam_unix(sshd:auth): check pass; user unknown",
                                       "Dec 10 07:55:55 LabSZ sshd[24331]: input_userauth_request: invalid user test [preauth]",
                                       "Dec 10 08:24:50 LabSZ sshd[24365]: pam_unix(sshd:auth): check pass; user unknown",])
    def test_cases_without_addresses(self, entry):
        assert not analyze_ssh_logs.get_ipv4s_from_log(parser.parse_entry(entry))

    @pytest.mark.parametrize("entry,expected_addresses",
                             [("Dec 10 07:27:55 LabSZ sshd[24237]: Received disconnect from 255.255.255.255: 11: Bye Bye [preauth]", ["255.255.255.255"]),
                              ("Dec 10 07:07:38 LabSZ sshd[24206]: Invalid user test9 from 0.0.0.0", ["0.0.0.0"])])
    def test_positive_corner_cases(self, entry, expected_addresses):
        assert analyze_ssh_logs.get_ipv4s_from_log(parser.parse_entry(entry)) == expected_addresses

    @pytest.mark.parametrize("entry",
                             ["Dec 10 07:27:55 LabSZ sshd[24237]: Received disconnect from 255.255.255.256: 11: Bye Bye [preauth]",
                              "Dec 10 07:27:55 LabSZ sshd[24237]: Received disconnect from 255.255.265.265",
                              "Dec 10 07:07:38 LabSZ sshd[24206]: Invalid user test9 from 0.800.0.0"])
    def test_negative_corner_cases(self, entry):
        assert not analyze_ssh_logs.get_ipv4s_from_log(parser.parse_entry(entry))

    @pytest.mark.xfail
    @pytest.mark.parametrize("entry,expected_matches",
                             [("Sends from host 1.1.1.1", "1.1.1.1"), ("Invalid address 255.0.0.0", "255.0.0.0"),
                              ("Hello from 199.199.18.1 Bye", "199.199.18.1"), ("Connecting from 255.249.239.9", "255.249.239.9")])
    def test_ipv4_pattern(self, entry, expected_matches):
        assert analyze_ssh_logs.IPV4_PATTERN.search(entry).group(1) == expected_matches


class TestGetUserFromLog:

    @pytest.mark.parametrize("entry,expected_user",
                             [("Dec 10 06:55:46 LabSZ sshd[24200]: Invalid user webmaster from 173.234.31.186", "webmaster"),
                              ("Dec 10 06:55:46 LabSZ sshd[24200]: input_userauth_request: invalid user webmaster [preauth]", "webmaster"),
                              ("Dec 10 06:55:46 LabSZ sshd[24200]: pam_unix(sshd:auth): check pass; user unknown", "unknown"),
                              ("Dec 10 07:07:45 LabSZ sshd[24206]: Failed password for invalid user test9 from 52.80.34.196 port 36060 ssh2", "test9"),
                              ("Dec 10 07:13:56 LabSZ sshd[24227]: PAM 5 more authentication failures; logname= uid=0 euid=0 tty=ssh ruser= rhost=5.36.59.76.dynamic-dsl-ip.omantel.net.om  user=root", "root"),
                              ("Dec 10 07:34:23 LabSZ sshd[24299]: Failed password for root from 123.235.32.19 port 57100 ssh2", "root"),
                              ("Dec 10 07:42:51 LabSZ sshd[24318]: Failed password for invalid user inspur from 183.136.162.51 port 55204 ssh2", "inspur"),
                              ("Dec 10 08:24:32 LabSZ sshd[24361]: input_userauth_request: invalid user  0101 [preauth]", "0101"),
                              ("Dec 12 14:20:38 LabSZ sshd[29040]: Accepted password for curi from 137.189.88.215 port 33299 ssh2", "curi"),
                              ("Dec 10 07:08:28 LabSZ sshd[24208]: reverse mapping checking getaddrinfo for ns.marryaldkfaczcz.com [173.234.31.186] failed - POSSIBLE BREAK-IN ATTEMPT!", "ns.marryaldkfaczcz.com")])
    def test_cases_with_users(self, entry, expected_user):
        actual_user = analyze_ssh_logs.get_user_from_log(parser.parse_entry(entry))
        assert actual_user == expected_user

    @pytest.mark.parametrize("entry",
                             ["Dec 10 07:07:38 LabSZ sshd[24206]: pam_unix(sshd:auth): authentication failure; logname= uid=0 euid=0 tty=ssh ruser= rhost=ec2-52-80-34-196.cn-north-1.compute.amazonaws.com.cn ",
                              "Dec 10 07:07:45 LabSZ sshd[24206]: Received disconnect from 52.80.34.196: 11: Bye Bye [preauth]",
                              "Dec 10 07:08:30 LabSZ sshd[24208]: Connection closed by 173.234.31.186 [preauth]",
                              "Dec 10 07:28:03 LabSZ sshd[24245]: pam_unix(sshd:auth): authentication failure; logname= uid=0 euid=0 tty=ssh ruser= rhost=112.95.230.3 ",
                              "Dec 11 08:30:45 LabSZ sshd[22341]: error: Received disconnect from 103.99.0.122: 14: No more user authentication methods available. [preauth]"])
    def test_cases_without_users(self, entry):
        assert not analyze_ssh_logs.get_user_from_log(parser.parse_entry(entry))


class TestMessageType:

    @pytest.mark.parametrize("entry", ["Dec 10 09:32:20 LabSZ sshd[24680]: Accepted password for fztu from 119.137.62.142 port 49116 ssh2"])
    def test_successful_login(self, entry):
        mess_type = analyze_ssh_logs.get_message_type(parser.parse_entry(entry))
        assert mess_type == analyze_ssh_logs.MessageType.SUCCESSFUL_LOGIN

    @pytest.mark.parametrize("entry", ["Dec 10 07:13:56 LabSZ sshd[24227]: PAM 5 more authentication failures; logname= uid=0 euid=0 tty=ssh ruser= rhost=5.36.59.76.dynamic-dsl-ip.omantel.net.om  user=root",
                                       "Dec 10 07:27:50 LabSZ sshd[24235]: pam_unix(sshd:auth): authentication failure; logname= uid=0 euid=0 tty=ssh ruser= rhost=112.95.230.3  user=root",
                                       "Dec 10 08:26:04 LabSZ sshd[24375]: PAM 1 more authentication failure; logname= uid=0 euid=0 tty=ssh ruser= rhost=5.188.10.180 ",
                                       "Dec 10 09:11:29 LabSZ sshd[24445]: pam_unix(sshd:auth): authentication failure; logname= uid=0 euid=0 tty=ssh ruser= rhost=103.99.0.122  user=root",
                                       "Dec 10 09:17:05 LabSZ sshd[24604]: input_userauth_request: invalid user redhat [preauth]",
                                       "Dec 10 09:16:48 LabSZ sshd[24595]: input_userauth_request: invalid user eoor [preauth]"])
    def test_unsuccessful_login(self, entry):
        mess_type = analyze_ssh_logs.get_message_type(parser.parse_entry(entry))
        assert mess_type == analyze_ssh_logs.MessageType.UNSUCCESSFUL_LOGIN

    @pytest.mark.parametrize("entry", ["Dec 10 06:55:48 LabSZ sshd[24200]: Connection closed by 173.234.31.186 [preauth]",
                                       "Dec 10 07:07:45 LabSZ sshd[24206]: Received disconnect from 52.80.34.196: 11: Bye Bye [preauth]",
                                       "Dec 10 08:33:26 LabSZ sshd[24385]: Received disconnect from 103.207.39.212: 11: Closed due to user request. [preauth]",
                                       "Dec 10 09:11:22 LabSZ sshd[24439]: error: Received disconnect from 103.99.0.122: 14: No more user authentication methods available. [preauth]",
                                       "Dec 10 09:45:06 LabSZ sshd[24761]: Received disconnect from 119.137.62.142: 11: disconnected by user",
                                       "Dec 10 11:48:13 LabSZ sshd[28523]: Disconnecting: Too many authentication failures for root [preauth]"])
    def test_closed_connection(self, entry):
        mess_type = analyze_ssh_logs.get_message_type(parser.parse_entry(entry))
        assert mess_type == analyze_ssh_logs.MessageType.CLOSED_CONNECTION

    @pytest.mark.parametrize("entry", ["Dec 10 07:27:52 LabSZ sshd[24235]: Failed password for root from 112.95.230.3 port 45378 ssh2",
                                       "Dec 10 06:55:48 LabSZ sshd[24200]: Failed password for invalid user webmaster from 173.234.31.186 port 38926 ssh2",
                                       "Dec 10 07:13:56 LabSZ sshd[24227]: message repeated 5 times: [ Failed password for root from 5.36.59.76 port 42393 ssh2]",
                                       "Dec 10 10:14:06 LabSZ sshd[24833]: Failed password for invalid user admin from 119.4.203.64 port 2191 ssh2"])
    def test_incorrect_password(self, entry):
        mess_type = analyze_ssh_logs.get_message_type(parser.parse_entry(entry))
        assert mess_type == analyze_ssh_logs.MessageType.INCORRECT_PASSWORD

    @pytest.mark.parametrize("entry", ["Dec 10 06:55:46 LabSZ sshd[24200]: Invalid user webmaster from 173.234.31.186",
                                       "Dec 10 09:07:23 LabSZ sshd[24415]: Invalid user 0 from 185.190.58.151",
                                       "Dec 10 09:48:23 LabSZ sshd[24806]: Failed none for invalid user 0 from 181.214.87.4 port 51889 ssh2"])
    def test_incorrect_username(self, entry):
        mess_type = analyze_ssh_logs.get_message_type(parser.parse_entry(entry))
        assert mess_type == analyze_ssh_logs.MessageType.INCORRECT_USERNAME

    @pytest.mark.parametrize("entry", ["Dec 10 06:55:46 LabSZ sshd[24200]: reverse mapping checking getaddrinfo for ns.marryaldkfaczcz.com [173.234.31.186] failed - POSSIBLE BREAK-IN ATTEMPT!",])
    def test_break_in_attempt(self, entry):
        mess_type = analyze_ssh_logs.get_message_type(parser.parse_entry(entry))
        assert mess_type == analyze_ssh_logs.MessageType.BREAK_IN_ATTEMPT

    @pytest.mark.parametrize("entry", ["Dec 10 06:55:46 LabSZ sshd[24200]: pam_unix(sshd:auth): check pass; user unknown",
                                       "Dec 10 07:13:56 LabSZ sshd[24227]: PAM service(sshd) ignoring max retries; 6 > 3",
                                       "Dec 10 07:35:15 LabSZ sshd[24303]: Did not receive identification string from 177.79.82.136",
                                       "Dec 10 09:32:20 LabSZ sshd[24680]: pam_unix(sshd:session): session opened for user fztu by (uid=0)",
                                       "Dec 10 09:45:06 LabSZ sshd[24680]: pam_unix(sshd:session): session closed for user fztu"])
    def test_others(self, entry):
        mess_type = analyze_ssh_logs.get_message_type(parser.parse_entry(entry))
        assert mess_type == analyze_ssh_logs.MessageType.OTHER


def test_exec_command_formatting():
    entry_log = parser.parse_entry("Dec 10 06:55:46 LabSZ sshd[24200]: Invalid user webmaster from 173.234.31.186")
    nmsp = Namespace(**{'ipv4': True, 'users': True, 'mstype': True})
    # output = app.exec_reg_commands(entry_log, nmsp)
    # assert output == "Analyze: Dec 10 06:55:46 LabSZ sshd[24200]: Invalid user webmaster from 173.234.31.186" \
      #                "\nIPv4 addresses: ['173.234.31.186']\nUsers: webmaster\nLog type: MessageType.INCORRECT_USERNAME"