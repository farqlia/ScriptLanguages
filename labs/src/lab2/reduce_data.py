import sys
from labs.src.lab2.parse_data import parse_log_line


def reduce_data(reduction):

    result = reduction(parse_log_line(sys.stdin.readline()))
    for line in sys.stdin:
        try:
            result = reduction(parse_log_line(line), result)
        except ValueError:
            sys.stderr.write(f"Couldn't parse line: {line}")

    return result