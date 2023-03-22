import sys
from typing import TextIO

import pytest
import datetime as dt

from labs.lab3.src.logs_reader import parse_log, read_logs
import labs.lab3.src as l
from labs.lab3.src.logs_sorting import sort_log


correct_cases = [('currypc.fpl.msstate.edu - - [22/Jul/1995:15:06:40 -0400] "GET /htbin/cdt_main.pl HTTP/1.0" 200 3714',
                           ('currypc.fpl.msstate.edu', dt.datetime(day=22, month=7, year=1995, hour=15, minute=6, second=40),
                            'GET', '/htbin/cdt_main.pl', 200, 3714)),
                                  ]


class TestParseLog:

    @pytest.mark.parametrize("line,fields",
                             correct_cases)
    def test_correct_cases(self, line, fields):

        assert parse_log(line) == fields


@pytest.fixture()
def prepare(tmp_path):

    f = tmp_path / "test.txt"
    file = open(f)

    [f.write_text(e) for e, _ in correct_cases]

    yield f
    file.close()


class TestReadLog:

    def test_correct_cases(self, prepare):
        assert len(read_logs(prepare)) == len(correct_cases)


class TestSortLogs:

    def test_sort_empty(self):
        assert sort_logs([]) == []