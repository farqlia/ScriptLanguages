from labs.src.lab2.reduce_data import reduce_data
from labs.src.lab2.filter_file_extensions import filter_file_extensions


def compute_graphics_fraction():

    def compute(log, accumulator=(0, 0)):
        return accumulator[0] + filter_file_extensions(log, 'gif', 'jpg', 'jpeg', 'xbm'), accumulator[1] + 1

    n_of_files_filtered, n_of_all_files = reduce_data(compute)

    return n_of_files_filtered / n_of_all_files


if __name__ == '__main__':
    print("{:.2f}".format(compute_graphics_fraction()))