from labs.src.lab2.filter_file_extensions import is_host_of_domain
from labs.src.lab2.filter_func import filter_lines


def filter_by_domain(*domains):

    inner_filter = lambda log: is_host_of_domain(log, *domains)

    return filter_lines(inner_filter)


if __name__ == '__main__':
    filter_by_domain('pl')