from labs.src.lab2.reduce_data import reduce_data


def log_with_max_resource():

    def comparison(log, accumulator=None):
        return log if not accumulator else (log if log.bytes > accumulator.bytes else accumulator)

    return reduce_data(comparison)


if __name__ == '__main__':
    log = log_with_max_resource()
    print(log.resource_path)
    print(log.bytes)