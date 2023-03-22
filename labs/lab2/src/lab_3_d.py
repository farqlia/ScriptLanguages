from labs.lab2.src.reduce_data import reduce_data
from labs.lab2.src.filter_file_extensions import is_resource_of_type


def compute_fraction(predicate):

    def compute(log, accumulator=(0, 0)):
        return accumulator[0] + predicate(log), accumulator[1] + 1

    n_of_files_filtered, n_of_all_files = reduce_data(compute)

    return n_of_files_filtered / n_of_all_files


def main():
    return compute_fraction(is_resource_of_type('gif', 'jpg', 'jpeg', 'xbm'))


if __name__ == '__main__':
    print("{:.2f}".format(main()))