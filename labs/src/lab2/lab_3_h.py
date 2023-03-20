from labs.src.lab2.filter_file_extensions import is_host_of_domain
from labs.src.lab2.filter_func import filter_lines


def filter_hosts_from_poland():
    return filter_lines(is_host_of_domain('pl'))


if __name__ == '__main__':
    filter_hosts_from_poland()