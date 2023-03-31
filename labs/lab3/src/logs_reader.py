import datetime
import re
import datetime as dt
import sys

REGEX = r"(?P<hostname>.+) - - \[(?P<date>.+) -\d+\] " \
        r"\"(?P<entry_details>.+)\" " \
        r"(?P<status_code>\d+) (?P<bytes>.+)"

DATE_FORMAT = "%d/%b/%Y:%H:%M:%S"

HOSTNAME_INDEX = 0
DATE_INDEX = 1
HTTP_METHOD_INDEX = 2
RESOURCE_PATH_INDEX = 3
STATUS_CODE_INDEX = 4
BYTES_INDEX = 5


def read_log(source=sys.stdin, error=sys.stderr):

    log = []
    for line in source:
        try:
            log.append(parse_entry(line))
        except ValueError:
            error.write(f"Couldn't parse: {line}")

    return log


def parse_entry(line):
    match = re.match(REGEX, line)

    if not match:
        raise ValueError(f"Invalid format found at line = {line}")

    try:
        entry_details = match.group('entry_details').split()
        http_method, resource_path = entry_details[0], entry_details[1]

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


def entry_to_dict(entry):

    try:
        dict_log = {

            'hostname': entry[HOSTNAME_INDEX],
            'date': entry[DATE_INDEX],
            'http method': entry[HTTP_METHOD_INDEX],
            'resource': entry[RESOURCE_PATH_INDEX],
            'status code': entry[STATUS_CODE_INDEX],
            'bytes': entry[BYTES_INDEX]

        }

    except IndexError:
        raise ValueError(f"Couldn't convert {entry}")
    else:
        return dict_log


def log_to_dict(logs):
    log_dict = {}
    for entry in logs:
        if entry[HOSTNAME_INDEX] not in log_dict:
            log_dict[entry[HOSTNAME_INDEX]] = []
        log_dict[entry[HOSTNAME_INDEX]].append(entry)
    return log_dict
