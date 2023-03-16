import re
from collections import namedtuple
import datetime as dt


REGEX = "(?P<hostname>.+) - - \[(?P<date>.+) -\d+\] \"(?P<log_details>.+)\" (?P<response_code>\d+) " \
        "(?P<bytes>\d+)"

DATE_FORMAT = "%d/%b/%Y:%H:%M:%S"

Log = namedtuple('Log', 'hostname date method resource_path response_code bytes')


def parse_log_line(line):

    match = re.match(REGEX, line)

    if not match:
        raise ValueError("Invalid format")

    try:
        log_details = match.group('log_details').split('\s+')
        http_method, resource_path = log_details[0], log_details[1]

        log = Log(hostname=match.group('hostname'),
                  date=dt.datetime.strptime(match.group('date'), DATE_FORMAT),
                  method=http_method,
                  resource_path=resource_path,
                  response_code=int(match.group('response_code')),
                  bytes=int(match.group('bytes')) if match.group('bytes').isdigit() else 0)
    except ValueError:
        raise ValueError("Invalid format")

    return log


