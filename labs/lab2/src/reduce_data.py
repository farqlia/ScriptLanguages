import sys
from labs.lab2.src.parse_data import parse_log_line


def reduce_data(reduction):

    result = reduction(parse_log_line(sys.stdin.readline()))
    for line in sys.stdin:
        try:
            result = reduction(parse_log_line(line), result)
        except ValueError:
            sys.stderr.write(f"Couldn't parse line: {line}")

    return result