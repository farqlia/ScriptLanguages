import labs.lab7.src.log_decorator as log_decorator
import pytest
import labs.lab5.src.ssh_user as ssh_user
import labs.lab5.src.regex_ssh_utilis as regex_ssh_utilis
import types


def test_type_of_definition():
    assert ssh_user.SSHUser.__class__ == type
    assert list.__class__ == type
    # assert sum.__class__ ==
    assert regex_ssh_utilis.get_error_cause.__class__ == types.FunctionType




