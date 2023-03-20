from labs.src.lab2.filter_func import filter_lines


def is_between_hours(start_hour, end_hour):

    if end_hour < start_hour:
        predicate = lambda h: h >= start_hour or h <= end_hour
    else:
        predicate = lambda h: h >= start_hour and h <= end_hour

    return predicate


def filter_by_hour():
    filter_lines(is_between_hours(22, 6))


if __name__ == '__main__':
    filter_by_hour()
