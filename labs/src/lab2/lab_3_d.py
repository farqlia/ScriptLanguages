from labs.src.lab2.reduce_data import reduce_data
from labs.src.lab2.filter_file_extensions import is_resource_of_type


def compute_fraction(predicate):

    def compute(log, accumulator=(0, 0)):
        return accumulator[0] + predicate(log), accumulator[1] + 1

    n_of_files_filtered, n_of_all_files = reduce_data(compute)

    return n_of_files_filtered / n_of_all_files


def compute_graphics_fraction():
    return compute_fraction(is_resource_of_type('gif', 'jpg', 'jpeg', 'xbm'))


if __name__ == '__main__':
    print("{:.2f}".format(compute_graphics_fraction()))