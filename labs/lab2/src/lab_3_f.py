from labs.lab2.src.filter_func import filter_lines


def is_between_hours(start_hour, end_hour):

    if end_hour < start_hour:
        predicate = lambda h: h >= start_hour or h < end_hour
    else:
        predicate = lambda h: start_hour <= h < end_hour

    def filter_inner(log):
        return predicate(log.date.hour)

    return filter_inner


def main():
    filter_lines(is_between_hours(22, 6))


if __name__ == '__main__':
    main()
