import datetime

import pytest
import labs.lab5.src.ssh_log_entry as ssh_log_entry
import labs.lab5.src.ssh_log_journal as ssh_log_journal
import ipaddress


class TestSSHLogJournal:
    pass

def test_generate_addresses():
    print(ssh_log_journal.generate_addresses(1))

class TestAcceptedPasswordJournal:

    instances = [
        "Dec 12 14:20:38 LabSZ sshd[29040]: Accepted password for curi from 137.189.88.215 port 33299 ssh2",
        "Dec 13 11:00:22 LabSZ sshd[5459]: Accepted password for zachary from 218.17.80.182 port 50313 ssh2",
        "Dec 15 10:38:57 LabSZ sshd[16980]: Failed password for zachary from 218.17.80.182 port 60110 ssh2",
        "Dec 16 17:02:11 LabSZ sshd[29026]: error: connect_to 10.10.34.41 port 22: failed."
    ]

    @pytest.fixture()
    def empty_instance(self):
        return ssh_log_journal.AcceptedPasswordJournal()

    @pytest.mark.parametrize("entry,result",
                             list(zip(instances,
                                      [True, True, False, False])))
    def test_only_accepted_password_instances(self, entry, result, empty_instance):
        assert bool(empty_instance.append(entry)) == result



class TestOtherJournal:

    instances = [
        "Dec 13 19:01:01 LabSZ sshd[6317]: Failed none for invalid user 0 from 181.214.87.4 port 42391 ssh2",
        "Jan  3 18:15:58 LabSZ sshd[5518]: pam_unix(sshd:auth): check pass; user unknown",
        "Jan  3 18:16:11 LabSZ sshd[5514]: PAM service(sshd) ignoring max retries; 6 > 3",
        "Dec 12 18:03:07 LabSZ sshd[30884]: pam_unix(sshd:session): session opened for user curi by (uid=0)",
        "Dec 12 17:58:45 LabSZ sshd[30879]: Connection closed by 5.188.10.180 [preauth]",
        "Dec 12 18:03:44 LabSZ sshd[31088]: Did not receive identification string from 195.154.37.122",
        "Dec 12 18:34:41 LabSZ sshd[31148]: input_userauth_request: invalid user wangj [preauth]",
        "Dec 19 19:53:50 LabSZ sshd[11934]: Invalid user admin from 185.222.209.151"
    ]

    @pytest.fixture()
    def empty_instance(self):
        return ssh_log_journal.OtherJournal()

    @pytest.fixture()
    def instance(self, empty_instance):
        for entry in TestOtherJournal.instances:
            empty_instance.append(entry)
        return empty_instance

    @pytest.mark.parametrize("entry", instances)
    def test_append_method(self, entry, empty_instance):
        assert empty_instance.append(entry)

    def test_length_method(self, instance):
        assert len(instance) == len(TestOtherJournal.instances)

    @pytest.mark.skip(reason="Day of month is with leading zero")
    def test_iterate(self, instance):
        for i, entry in enumerate(instance):
            print(entry, ".")
            assert entry == ssh_log_entry.Other(TestOtherJournal.instances[i])

    def test_iterate_2(self, instance):
        i = 0
        for entry in instance:
            assert entry.message == ssh_log_entry.Other(TestOtherJournal.instances[i]).message
            i += 1

        assert i == len(TestOtherJournal.instances)

    def test_filter(self, instance):

        in_jan = lambda e: e.date.month == 1
        filtered = instance.filter(in_jan)
        assert filtered == [ssh_log_entry.Other("Jan  3 18:15:58 LabSZ sshd[5518]: pam_unix(sshd:auth): check pass; user unknown"),
                            ssh_log_entry.Other("Jan  3 18:16:11 LabSZ sshd[5514]: PAM service(sshd) ignoring max retries; 6 > 3")]

    @pytest.mark.parametrize("ipv4_address,expected",
                             [("181.214.87.4", [ssh_log_entry.Other(instances[0])]),
                              ("0.0.0.0", [])])
    def test_filter_for_ip(self, ipv4_address, expected, instance):
        assert instance.filter_for_ip(ipv4_address) == expected

    def test_slicing_by_index(self, instance):
        # print(slice(1, 2, 3).indices(3))
        assert instance[0:-1] == list(map(lambda l: ssh_log_entry.Other(l), TestOtherJournal.instances[0:-1]))
        assert instance[0] == ssh_log_entry.Other(TestOtherJournal.instances[0])
        assert instance[:2] == [ssh_log_entry.Other(TestOtherJournal.instances[0]),
                                ssh_log_entry.Other(TestOtherJournal.instances[1])]
        assert instance[::-1] == list(map(lambda l: ssh_log_entry.Other(l), TestOtherJournal.instances[::-1]))

    def test_slicing_by_ipv4_address(self, instance):
        assert instance[ipaddress.IPv4Address("182.0.0.0"):] == [ssh_log_entry.Other(TestOtherJournal.instances[-3]),
                                                                  ssh_log_entry.Other(TestOtherJournal.instances[-1])]
        assert instance[ipaddress.IPv4Address("195.154.37.122")] == [ssh_log_entry.Other(TestOtherJournal.instances[-3])]
        assert instance[:ipaddress.IPv4Address("5.255.255.255")] == [ssh_log_entry.Other(TestOtherJournal.instances[-4])]
        print(instance[ipaddress.IPv4Address("0.0.0.0"):ipaddress.IPv4Address("255.255.255.255"):2])


    def test_slicing_by_date(self, instance):
        assert instance[datetime.datetime(year=2023, month=1, day=1):datetime.datetime(year=2023, month=1, day=10)] \
               == [ssh_log_entry.Other(TestOtherJournal.instances[1]), ssh_log_entry.Other(TestOtherJournal.instances[2])]

        assert instance[:datetime.datetime(year=2022, month=12, day=15)] == \
               list(map(lambda l: ssh_log_entry.Other(l),
                        [TestOtherJournal.instances[0], TestOtherJournal.instances[3],
                TestOtherJournal.instances[4], TestOtherJournal.instances[5],
                TestOtherJournal.instances[6]]))

        assert instance[datetime.datetime(year=2023, month=1, day=1):] == \
               [ssh_log_entry.Other(TestOtherJournal.instances[1]),
                ssh_log_entry.Other(TestOtherJournal.instances[2])]
