from labs.lab2.src.filter_file_extensions import is_host_of_domain
from labs.lab2.src.filter_func import filter_lines


def main():
    return filter_lines(is_host_of_domain('pl'))


if __name__ == '__main__':
    main()