import sys
from os import environ


def print_sorted_variables(env_vars):
    for env in sorted(env_vars):
        print(f"{env} = {environ[env]}")


def filter_env_vars():
    return [sys_arg.upper() for sys_arg in sys.argv[1:] if sys_arg.upper() in environ]


def any_argument():
    return len(sys.argv) > 1


if __name__ == "__main__":
    print_sorted_variables(filter_env_vars() if any_argument() else environ)
