from labs.src.lab2.filter_func import filter_lines

day_of_week = 5

def filter_by_day(day_number):

    def filter(log):
        return log.date.isoweekday() == day_number

    return filter_lines(filter)


if __name__ == '__main__':
    filter_by_day(day_of_week)