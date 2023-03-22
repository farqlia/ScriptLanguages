from labs.lab2.src.filter_func import filter_lines
from labs.lab2.src.filter_response_code import filter_response_code

if __name__ == '__main__':
    filter_lines(filter_response_code(200))