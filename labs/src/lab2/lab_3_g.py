from labs.src.lab2.filter_func import filter_lines


def filter_by_day(day_number):

    def filter(log):
        return log.date.isoweekday() == day_number

    return filter_lines(filter)


def filter_from_friday():
    day_of_week = 5
    filter_by_day(day_of_week)


if __name__ == '__main__':
    filter_from_friday()