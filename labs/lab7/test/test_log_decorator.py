import labs.lab7.src.log_decorator as log_decorator
import pytest
import labs.lab5.src.ssh_user as ssh_user
import labs.lab5.src.regex_ssh_utilis as regex_ssh_utilis
import types


def test_type_of_definition():
    assert ssh_user.SSHUser.__class__ == type
    assert list.__class__ == type
    assert int.__class__ == type
    assert sorted.__class__ == types.BuiltinFunctionType
    # assert sum.__class__ ==
    lab = lambda x: x + 2
    assert lab.__class__ == types.FunctionType
    assert regex_ssh_utilis.get_error_cause.__class__ == types.FunctionType




