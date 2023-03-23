import sys
from typing import TextIO

import pytest
import datetime as dt

from labs.lab3.src.logs_reader import parse_log, read_logs, log_to_dict
import labs.lab3.src.logs_reader as lr
from labs.lab3.src.logs_utilities import sort_log
import labs.lab3.src.logs_utilities as log_utils

class TestParseLog:

    correct_cases = [('currypc.fpl.msstate.edu - - [22/Jul/1995:15:06:40 -0400] "GET /htbin/cdt_main.pl HTTP/1.0" 200 3714',
                      ('currypc.fpl.msstate.edu', dt.datetime(day=22, month=7, year=1995, hour=15, minute=6, second=40),
                       'GET', '/htbin/cdt_main.pl', 200, 3714)),
                     ]
    @pytest.mark.parametrize("line,fields",
                             correct_cases)
    def test_correct_cases(self, line, fields):

        assert parse_log(line) == fields


class TestReadLog:

    test_logs = ['currypc.fpl.msstate.edu - - [22/Jul/1995:15:06:40 -0400] "GET /htbin/cdt_main.pl HTTP/1.0" 200 3714',
                 'burger.letters.com - - [01/Jul/1995:00:00:11 -0400] "GET /shuttle/countdown/liftoff.html HTTP/1.0" 304 1',
                 'unicomp6.unicomp.net - - [01/Jul/1995:00:00:14 -0400] "GET /images/KSC-logosmall.gif HTTP/1.0" 200 1204',
                 'rima.ccsi.com - - [22/Jul/1995:15:07:00 -0400] "GET /persons/astronauts/m-to-p/pogueWR.txt HTTP/1.0" 404 -']

    @pytest.fixture()
    def prepare(self, tmp_path):
        f = tmp_path / "test.txt"
        [f.write_text(e) for e in self.test_logs]

        yield f

    def test_correct_cases(self, prepare):
        assert len(read_logs(self.test_logs)) == len(self.test_logs)


class TestSortLogs:

    test_logs = ['currypc.fpl.msstate.edu - - [22/Jul/1995:15:06:40 -0400] "GET /htbin/cdt_main.pl HTTP/1.0" 200 3714',
                 'burger.letters.com - - [01/Jul/1995:00:00:11 -0400] "GET /shuttle/countdown/liftoff.html HTTP/1.0" 304 1',
                 'unicomp6.unicomp.net - - [01/Jul/1995:00:00:14 -0400] "GET /images/KSC-logosmall.gif HTTP/1.0" 200 1204',
                 'rima.ccsi.com - - [22/Jul/1995:15:07:00 -0400] "GET /persons/astronauts/m-to-p/pogueWR.txt HTTP/1.0" 404 -']

    def test_sort_empty(self):
        assert sort_log([], lambda log: log[1]) == []

    @pytest.mark.parametrize("i", [-1, 10])
    def test_for_illegal_index(self, i):
        logs = read_logs(self.test_logs)
        with pytest.raises(IndexError):
            sort_log(logs, i)

    def test_sorting_logs(self):
        logs = read_logs(self.test_logs)
        sorted_by_size = [logs[3], logs[1], logs[2], logs[0]]
        assert sort_log(logs, lr.BYTES_INDEX) == sorted_by_size


@pytest.mark.xfail
class TestGetEntriesByAddr:

    test_logs = ['onyx.southwind.net - - [01/Jul/1995:00:01:34 -0400] "GET /shuttle/countdown/countdown.html HTTP/1.0" 200 3985',
                 'onyx.southwind.net - - [01/Jul/1995:00:01:35 -0400] "GET /shuttle/countdown/count.gif HTTP/1.0" 202 40310',
                 'onyx.southwind.net - - [01/Jul/1995:00:01:39 -0400] "GET /images/KSC-logosmall.gif HTTP/1.0" 304 0',
                 'rima.ccsi.com - - [22/Jul/1995:15:07:00 -0400] "GET /persons/astronauts/m-to-p/pogueWR.txt HTTP/1.0" 404 -']

    def test_for_successful_code(self):
        logs = read_logs(self.test_logs)
        assert log_utils.get_entries_by_addr("onyx.southwind.net",
                                             logs) == [logs[0], logs[1]]

    def test_for_unsuccesful_code(self):
        assert log_utils.get_entries_by_addr("rima.ccsi.com",
                                             read_logs(self.test_logs)) == []


class TestGetEntriesByCode:
    test_logs = [
        'onyx.southwind.net - - [01/Jul/1995:00:01:34 -0400] "GET /shuttle/countdown/countdown.html HTTP/1.0" 200 3985',
        'onyx.southwind.net - - [01/Jul/1995:00:01:35 -0400] "GET /shuttle/countdown/count.gif HTTP/1.0" 200 40310',
        'onyx.southwind.net - - [01/Jul/1995:00:01:39 -0400] "GET /images/KSC-logosmall.gif HTTP/1.0" 304 0',
        'rima.ccsi.com - - [22/Jul/1995:15:07:00 -0400] "GET /persons/astronauts/m-to-p/pogueWR.txt HTTP/1.0" 404 -']

    def test_for_200_code(self):
        logs = read_logs(self.test_logs)
        assert log_utils.get_entries_by_code(200,
                                             logs) == [logs[0], logs[1]]

    def test_for_500_code(self):
        assert log_utils.get_entries_by_code(500,
                                             read_logs(self.test_logs)) == []


class TestGetFailedReads:

    test_logs = [
        'onyx.southwind.net - - [01/Jul/1995:00:01:34 -0400] "GET /shuttle/countdown/countdown.html HTTP/1.0" 403 -',
        'onyx.southwind.net - - [01/Jul/1995:00:01:35 -0400] "GET /shuttle/countdown/count.gif HTTP/1.0" 500 -',
        'onyx.southwind.net - - [01/Jul/1995:00:01:39 -0400] "GET /images/KSC-logosmall.gif HTTP/1.0" 512 -',
        'rima.ccsi.com - - [22/Jul/1995:15:07:00 -0400] "GET /persons/astronauts/m-to-p/pogueWR.txt HTTP/1.0" 404 -',
        'unicomp6.unicomp.net - - [01/Jul/1995:00:00:14 -0400] "GET /images/NASA-logosmall.gif HTTP/1.0" 200 786']

    def test_for_merged_failed_reads(self):
        logs = read_logs(self.test_logs)
        assert log_utils.get_failed_reads(logs, merged=True) == [logs[0], logs[3], logs[1], logs[2]]

    def test_for_split_failed_reads(self):
        logs = read_logs(self.test_logs)
        logs_4xx, logs_5xx = log_utils.get_failed_reads(logs, merged=False)
        assert logs_4xx == [logs[0], logs[3]]
        assert logs_5xx == [logs[1], logs[2]]


class TestGetEntriesByExtension:
    test_logs = [
        'onyx.southwind.net - - [01/Jul/1995:00:01:34 -0400] "GET /shuttle/countdown/countdown.html HTTP/1.0" 403 -',
        'onyx.southwind.net - - [01/Jul/1995:00:01:35 -0400] "GET /shuttle/countdown/count.gif HTTP/1.0" 500 -',
        'vm.marist.edu - - [22/Jul/1995:15:19:58 -0400] "GET /history/astp/flight-summary.txt" 200 509',
        'rima.ccsi.com - - [22/Jul/1995:15:07:00 -0400] "GET /persons/astronauts/m-to-p/pogueWR.txt HTTP/1.0" 404 -',
        'unicomp6.unicomp.net - - [01/Jul/1995:00:00:14 -0400] "GET /images/NASA-logosmall.gif HTTP/1.0" 200 786']

    def test_for_extension(self):
        logs = read_logs(self.test_logs)
        assert log_utils.get_entries_by_extension(logs, 'gif', 'html') == [logs[0], logs[1], logs[4]]


class TestLogToDict:

    test_logs = [
        'onyx.southwind.net - - [01/Jul/1995:00:01:34 -0400] "GET /shuttle/countdown/countdown.html HTTP/1.0" 403 -',
        'onyx.southwind.net - - [01/Jul/1995:00:01:35 -0400] "GET /shuttle/countdown/count.gif HTTP/1.0" 200 -',
        'onyx.southwind.net - - [01/Jul/1995:00:01:39 -0400] "GET /images/KSC-logosmall.gif HTTP/1.0" 512 -',
        'rima.ccsi.com - - [22/Jul/1995:15:07:00 -0400] "GET /persons/astronauts/m-to-p/pogueWR.txt HTTP/1.0" 404 -']

    def test_convert_to_dict(self):
        logs = read_logs(self.test_logs)
        assert log_to_dict(logs) == {'onyx.southwind.net': logs[:3], 'rima.ccsi.com': [logs[3]]}

    def test_get_addr(self):
        logs = log_to_dict(read_logs(self.test_logs))
        assert set(log_utils.get_addrs(logs)) == {'onyx.southwind.net', 'rima.ccsi.com'}

    def test_printing(self):
        logs = log_to_dict(read_logs(self.test_logs))
        key = 'onyx.southwind.net'
        assert log_utils.string_dict_entry_dates(key, logs[key]) == "onyx.southwind.net sent 3 queries between 01/07/1995" \
                                                                    " and 01/07/1995 with 33.0% successful responses."