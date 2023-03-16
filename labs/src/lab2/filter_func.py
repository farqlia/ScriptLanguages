import sys
from labs.src.lab2.parse_data import parse_log_line


def filter_data(predicate):

    data = ""
    for line in sys.stdin:
        try:
            if predicate(parse_log_line(line)):
                data += line + "\n"
        except ValueError:
            sys.stderr.write(f"Couldn't parse line: {line}")

    return data