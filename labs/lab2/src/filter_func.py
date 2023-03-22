import sys
from labs.lab2.src.parse_data import parse_log_line


def filter_lines(predicate):

    for line in sys.stdin:
        try:
            if predicate(parse_log_line(line)):
                print(line.rstrip())
        except ValueError:
            sys.stderr.write(f"Couldn't parse line: {line}")
