from argparse import Namespace

import pandas as pd
from pathlib import Path
from os import getcwd
import pytest
import re
import labs.ssh_logs_program.src.model.regex_ssh_utilis as analyze_ssh_logs
import labs.ssh_logs_program.src.model.ssh_logs_prepare as ssh_logs_prepare
from collections import namedtuple
import time
import labs.ssh_logs_program.src.model.app as app
import datetime


class TestParseEntry:

    @pytest.fixture(scope='session')
    def parser(self):
        return ssh_logs_prepare.Parser()

    @pytest.mark.parametrize("log,expected_groups",
                             [("Dec 10 06:55:46 LabSZ sshd[24200]: Invalid user webmaster from 173.234.31.186",
                               {'date': 'Dec 10 06:55:46',
                                'pid': '24200', 'message': 'Invalid user webmaster from 173.234.31.186'})])
    def test_pattern_for_parsing_logs(self, log, expected_groups, parser):
        match = re.match(ssh_logs_prepare.Parser.PATTERN, log)
        assert all(expected_groups[k] == match.group(k) for k in expected_groups.keys())

    @pytest.mark.parametrize("entry,expected",
                             [("Dec 10 07:13:43 LabSZ sshd[24227]: Failed password for root from 5.36.59.76 port 42393 ssh2"
                               , {'date': datetime.datetime(year=2022, month=12, day=10, hour=7, minute=13, second=43),
                                  'host': 'LabSZ', 'pid': 24227,
                                  'message': 'Failed password for root from 5.36.59.76 port 42393 ssh2'}),
                              ])
    def test_convert_to_namedtuple(self, entry, expected, parser):
        tuple_entry = parser.parse_entry(entry)
        assert tuple_entry.date == expected['date']
        assert tuple_entry.host == expected['host']
        assert tuple_entry.pid == expected['pid']
        assert tuple_entry.message == expected['message']
        assert len(tuple_entry) == len(expected)
