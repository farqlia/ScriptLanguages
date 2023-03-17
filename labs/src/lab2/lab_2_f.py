from labs.src.lab2.filter_func import filter_lines


def filter_between_hours(start_hour, end_hour):

    predicate = None
    if end_hour < start_hour:
        predicate = lambda h: h >= start_hour or h <= end_hour
    else:
        predicate = lambda h: h >= start_hour and h <= end_hour

    def filter(log):
        return predicate(log.date.hour)

    return filter_lines(filter)


if __name__ == '__main__':
    filter_between_hours(22, 6)
