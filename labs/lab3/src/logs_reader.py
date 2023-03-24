import datetime
import re
import datetime as dt
import sys

REGEX = r"(?P<hostname>.+) - - \[(?P<date>.+) -\d+\] " \
        r"\"(?P<log_details>.+)\" " \
        r"(?P<status_code>\d+) (?P<bytes>.+)"

DATE_FORMAT = "%d/%b/%Y:%H:%M:%S"

HOSTNAME_INDEX = 0
DATE_INDEX = 1
HTTP_METHOD_INDEX = 2
RESOURCE_PATH_INDEX = 3
STATUS_CODE_INDEX = 4
BYTES_INDEX = 5


def read_logs(source=sys.stdin, error=sys.stdin):

    log = []
    for line in source:
        try:
            log.append(parse_log(line))
        except ValueError:
            error.write(f"Couldn't parse: {line}")

    return log


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
               int(match.group('status_code')),
               int(match.group('bytes')) if match.group('bytes').isdigit() else 0)

    except ValueError:
        raise ValueError(f"Invalid format found at line = {line}")
    except IndexError:
        raise ValueError(f"Invalid format found at line = {line}")

    return log


def entry_to_dict(log):

    try:
        dict_log = {

            'hostname': log[HOSTNAME_INDEX],
            'date': log[DATE_INDEX],
            'http method': log[HTTP_METHOD_INDEX],
            'resource': log[RESOURCE_PATH_INDEX],
            'status code': log[STATUS_CODE_INDEX],
            'bytes': log[BYTES_INDEX]

        }

    except IndexError:
        raise ValueError(f"Couldn't convert {log}")
    else:
        return dict_log


def log_to_dict(log):

    log_dict = {}
    for l in log:
        if l[HOSTNAME_INDEX] not in log_dict:
            log_dict[l[HOSTNAME_INDEX]] = []
        log_dict[l[HOSTNAME_INDEX]].append(l)
    return log_dict
