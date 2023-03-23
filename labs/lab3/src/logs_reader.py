import re
import datetime as dt
import sys

REGEX = r"(?P<hostname>.+) - - \[(?P<date>.+) -\d+\] " \
        r"\"(?P<log_details>.+)\" " \
        r"(?P<response_code>\d+) (?P<bytes>.+)"

DATE_FORMAT = "%d/%b/%Y:%H:%M:%S"

HOSTNAME_INDEX = 0
DATE_INDEX = 1
HTTP_METHOD_INDEX = 2
RESOURCE_PATH_INDEX = 3
RESPONSE_CODE_INDEX = 4
BYTES_INDEX = 5

def read_logs(source=sys.stdin):

    logs = []
    for line in source:
        try:
            logs.append(parse_log(line))
        except ValueError as e:
            sys.stderr.write(e.message)

    return logs


def parse_log(line):
    match = re.match(REGEX, line)

    if not match:
        raise ValueError(f"Invalid format found at line = {line}")

    try:
        log_details = match.group('log_details').split()
        http_method, resource_path = log_details[0], log_details[1]

        log = (match.group('hostname'),
               dt.datetime.strptime(match.group('date'), DATE_FORMAT),
               http_method,
               resource_path,
               int(match.group('response_code')),
               int(match.group('bytes')) if match.group('bytes').isdigit() else 0)

    except ValueError:
        raise ValueError(f"Invalid format found at line = {line}")
    except IndexError:
        raise ValueError(f"Invalid format found at line = {line}")

    return log

