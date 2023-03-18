from labs.src.lab2.reduce_data import reduce_data


def count_logs_with_response_code(response_code):

    def count(log, accumulator=0):
        return accumulator + (log.response_code == response_code)

    return reduce_data(count)