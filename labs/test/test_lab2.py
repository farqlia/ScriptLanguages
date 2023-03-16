import re
from collections import namedtuple
import datetime as dt
import pytest
from labs.src.lab2.parse_data import parse_log_line, REGEX, DATE_FORMAT

log_regex = REGEX

def test_pattern_matching():
    log = 'ppp-mia-30.shadow.net - - [01/Jul/1995:00:00:27 -0400] "GET / HTTP/1.0" 200 7074'
    match = re.match(log_regex, log)
    assert match.group('hostname') == 'ppp-mia-30.shadow.net'
    assert match.group('date') == '01/Jul/1995:00:00:27'
    assert match.group('log_details') == 'GET / HTTP/1.0'
    assert match.group('response_code') == '200'
    assert match.group('bytes') == '7074'

    print(match.groups())


@pytest.mark.parametrize("log,mess", [('- - [01/Jul/1995:00:00:27 -0400] "GET / HTTP/1.0" 200 7074', 'missing hostname'),
                                 ('ppp-mia-30.shadow.net [01/Jul/1995:00:00:27 -0400] "GET / HTTP/1.0" 200 7074', 'missing - -'),
                                      ('ppp-mia-30.shadow.net - - [01/Jul/1995:00:00:27 -0400] "GET / HTTP/1.0" 7074', 'missing response code'),
                                      ('ppp-mia-30.shadow.net - - [01/Jul/1995:00:00:27 -0400] "GET / HTTP/1.0" 200', 'missing bytes')])
def test_invalid_input_for_pattern_matching(log, mess):
    match = re.match(log_regex, log)
    assert not match, mess


def test_namedtuple():

    Point = namedtuple('Point', 'x y')

    p = Point(2, 4)

    assert p.x == 2
    assert p.y == 4

dt_format = DATE_FORMAT

def test_datetime_conversion():
    actual = dt.datetime.strptime('01/Jul/1995:00:00:27', dt_format)

    expected = dt.datetime(year=1995, month=7, day=1, hour=0, minute=0, second=27)
    assert expected == actual


def test_invalid_datetime_conversion():

    with pytest.raises(ValueError):
        dt.datetime.strptime('01//1995:00:00:27', dt_format)


def test_protocol_info():

    protocol_format = "(?P<method>.+) (?P<resource_path>.+) (?P<protocol_version>.+)"

    match = re.match(protocol_format, 'GET / HTTP/1.0')

    assert match.group('method') == 'GET'
    assert match.group('resource_path') == '/'
    assert match.group('protocol') == 'HTTP/1.0'


@pytest.mark.parametrize("log", ['ppp-nyc-2-36.ios.com - - [22/Jul/1995:15:06:43 -0400] "GET /shuttle/missions/51-l/sounds/ HTTP/1.0" 200 -',
                                 'dal28.onramp.net - - [21/Jul/1995:23:03:36 -0400] "GET /cgi-bin/imagemap/countdown70?259,240 HTTP/1.0" 302 97'])
def test_valid_input_for_log_conversion(log):
    assert parse_log_line(log)

@pytest.mark.parametrize("log,mess", [('- - [01/Jul/1995:00:00:27 -0400] "GET / HTTP/1.0" 200 7074', 'missing hostname'),
                                 ('ppp-mia-30.shadow.net [01/Jul/1995:00:00:27 -0400] "GET / HTTP/1.0" 200 7074', 'missing - -'),
                                    ('ppp-mia-30.shadow.net - - [01//1995:00:00:27 -0400] "GET / HTTP/1.0" 200 7074', 'missing month name'),
                                      ('ppp-mia-30.shadow.net - - [01/Jul/1995:00:00:27 -0400] " / HTTP/1.0" 200 7074', 'missing http method'),
                                      ('ppp-mia-30.shadow.net - - [01/Jul/1995:00:00:27 -0400] "GET HTTP/1.0" 200 7074', 'missing resource path'),
                                      ('ppp-mia-30.shadow.net - - [01/Jul/1995:00:00:27 -0400] "GET / " 200 7074', 'missing protocol version'),
                                      ('ppp-mia-30.shadow.net - - [01/Jul/1995:00:00:27 -0400] "GET / HTTP/1.0" 7074', 'missing response code'),
                                      ('ppp-mia-30.shadow.net - - [01/Jul/1995:00:00:27 -0400] "GET / HTTP/1.0" 200', 'missing bytes')])
def test_invalid_input_for_log_conversion(log, mess):

    with pytest.raises(ValueError):
        parse_log_line(log)


def test_for_numeric():
    assert "5466".isdigit()