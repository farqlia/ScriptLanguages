from labs.src.lab2.reduce_data import reduce_data

gigabyte_in_bytes = 1073741824


def sum_bytes(conversion_unit=1):

    def sum(log, accumulator=0):
        return log.bytes + accumulator

    return reduce_data(sum) / conversion_unit


print(sum_bytes(gigabyte_in_bytes))