import pytest
import labs.lab5.src.ssh_log_entry as ssh_log_entry
import datetime
from ipaddress import IPv4Address

from labs.lab5.src.ssh_logs_prepare import Parser


# Dec 14 16:02:42 LabSZ sshd[10327]: fatal: Read from socket failed: Connection reset by peer [preauth] ??

class TestSSHLogEntry:

    instance = "Dec 12 14:20:38 LabSZ sshd[29040]: Accepted password for curi from 137.189.88.215 port 33299 ssh2"

    def test_properties(self):
        instance = ssh_log_entry.AcceptedPassword(TestSSHLogEntry.instance)
        assert instance.date == datetime.datetime(year=2022, month=12, day=12, hour=14, minute=20, second=38)
        assert instance.message == "Accepted password for curi from 137.189.88.215 port 33299 ssh2"
        assert instance.pid == 29040
        assert instance.host == "LabSZ"
        assert instance.has_ip

        # no access to _message
        # instance.message

    def test_magic_methods(self):
        instance = ssh_log_entry.AcceptedPassword(TestSSHLogEntry.instance)
        assert instance.__repr__() == "Dec 12 14:20:38 LabSZ sshd[29040]: Accepted password for curi from 137.189.88.215 port 33299 ssh2"
        other_instance = ssh_log_entry.AcceptedPassword(TestSSHLogEntry.instance)
        assert instance.__eq__(other_instance)
        recent_entry = "Dec 13 20:41:43 LabSZ sshd[29040]: Accepted password for fztu from 119.137.63.195 port 49267 ssh2"
        assert ssh_log_entry.AcceptedPassword(recent_entry) > instance



class TestAcceptedPassword:

    instances_to_test = [
        "Dec 12 14:20:38 LabSZ sshd[29040]: Accepted password for curi from 137.189.88.215 port 33299 ssh2",
        "Dec 13 11:00:22 LabSZ sshd[5459]: Accepted password for zachary from 218.17.80.182 port 50313 ssh2",
        "Dec 13 19:03:16 LabSZ sshd[6320]: Accepted password for fztu from 119.137.63.195 port 62430 ssh2",
        "Dec 13 20:41:43 LabSZ sshd[7056]: Accepted password for fztu from 119.137.63.195 port 49267 ssh2",
    ]

    @pytest.mark.ignore
    @pytest.mark.parametrize("entry",
                             ["Accepted password for curi from 137.189.88.215 port 33299 ssh2"])
    def test_validate(self, entry):
        pass

    def test_accepted_password_properties(self):
        instance = ssh_log_entry.AcceptedPassword(TestAcceptedPassword.instances_to_test[1])
        assert instance.user == "zachary"
        assert instance.get_ipv4_address() == IPv4Address("218.17.80.182")
        assert instance.port == 50313


class TestFailedPassword:

    instances_to_test = [
        "Dec 13 11:00:21 LabSZ sshd[5459]: Failed password for zachary from 218.17.80.182 port 50313 ssh2",
        "Dec 13 19:13:22 LabSZ sshd[6447]: Failed password for root from 203.190.163.125 port 34400 ssh2",
        "Dec 14 04:31:27 LabSZ sshd[8027]: Failed password for root from 180.101.249.16 port 54864 ssh2",
        "Dec 15 10:38:57 LabSZ sshd[16980]: Failed password for zachary from 218.17.80.182 port 60110 ssh2",
        "Dec 15 10:39:03 LabSZ sshd[16980]: Failed password for zachary from 218.17.80.182 port 60110 ssh2",
        "Jan  3 18:17:18 LabSZ sshd[5541]: message repeated 5 times: [ Failed password for root from 59.63.188.30 port 46543 ssh2]",
    ]

    @pytest.mark.parametrize("entry,properties",
                             [(instances_to_test[0], ("zachary", IPv4Address("218.17.80.182"), 50313)),
                              (instances_to_test[-1], ("root", IPv4Address("59.63.188.30"), 46543))])
    def test_failed_password_properties(self, entry, properties):
        instance = ssh_log_entry.FailedPassword(entry)
        assert instance.user == properties[0]
        assert instance.get_ipv4_address() == properties[1]
        assert instance.port == properties[2]


class Error:

    instances_to_test = [
        "Dec 16 14:25:57 LabSZ sshd[27703]: error: Received disconnect from 103.79.141.133: 3: com.jcraft.jsch.JSchException: Auth fail [preauth]",
        "Dec 16 17:02:11 LabSZ sshd[29026]: error: connect_to 10.10.34.41 port 22: failed.",
        "Dec 17 05:17:45 LabSZ sshd[25192]: error: Received disconnect from 103.99.0.122: 14: No more user authentication methods available. [preauth]",
        "Jan  4 13:42:21 LabSZ sshd[32136]: error: Received disconnect from 212.83.176.1: 3: org.vngx.jsch.userauth.AuthCancelException: User authentication canceled by user [preauth]",
        "Jan  5 09:47:34 LabSZ sshd[17423]: error: Received disconnect from 195.154.45.62: 3: com.jcraft.jsch.JSchException: timeout in waiting for rekeying process. [preauth]"
    ]

    @pytest.mark.parametrize("entry,properties",
                             [
                                 (instances_to_test[0], (IPv4Address("103.79.141.133"), "received disconnect: auth fail")),
                                 (instances_to_test[1], (IPv4Address("10.10.34.41"), "connection: failed")),
                                 (instances_to_test[2], (IPv4Address("103.99.0.122"), "received disconnect: no more user authentication methods available")),
                                 (instances_to_test[3], (IPv4Address("212.83.176.1"), "received disconnect: user authentication canceled by user")),
                                 (instances_to_test[4], (IPv4Address("195.154.45.62")), "received disconnect: timeout in waiting for rekeying process")
                             ])
    def test_error_properties(self, entry, properties):
        instance = ssh_log_entry.Error(entry)
        assert instance.cause == properties[1]
        assert instance.get_ipv4_address() == properties[0]

# Ignore for now
class Other:

    instances_to_test = [
        "Dec 13 19:01:01 LabSZ sshd[6317]: Failed none for invalid user 0 from 181.214.87.4 port 42391 ssh2",
        "Jan  3 18:15:58 LabSZ sshd[5518]: pam_unix(sshd:auth): check pass; user unknown",
        "Jan  3 18:16:11 LabSZ sshd[5514]: PAM service(sshd) ignoring max retries; 6 > 3",
    ]

    @pytest.mark.parametrize("entry,has_address",
                             list(zip(instances_to_test,
                                      [True, False, False])))
    def test_other_properties(self, entry, has_address):
        instance = ssh_log_entry.Other(entry)
        assert bool(instance.get_ipv4_address()) == has_address



