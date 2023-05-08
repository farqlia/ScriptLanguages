import logging
import time

import labs.lab7.src.log_decorator as log_decorator
import pytest
import labs.lab5.src.ssh_user as ssh_user
import labs.lab5.src.regex_ssh_utilis as regex_ssh_utilis
import types
import inspect


def test_type_of_definition():
    assert ssh_user.SSHUser.__class__ == type
    assert inspect.isclass(ssh_user.SSHUser)
    assert list.__class__ == type
    assert inspect.isclass(list)
    assert int.__class__ == type
    assert inspect.isclass(int)
    assert sorted.__class__ == types.BuiltinFunctionType
    # assert inspect.(sorted)
    # assert isinstance(sorted, callable())
    # assert sum.__class__ ==
    lab = lambda x: x + 2
    assert lab.__class__ == types.FunctionType
    assert inspect.isfunction(lab)
    assert regex_ssh_utilis.get_error_cause.__class__ == types.FunctionType
    assert inspect.isfunction(regex_ssh_utilis.get_error_cause)


def test_log_decorator():

    def slow_function():
        time.sleep(3)
        print("Finished")

    slow_f = log_decorator.log(logging.WARNING)(slow_function)
    slow_f()


