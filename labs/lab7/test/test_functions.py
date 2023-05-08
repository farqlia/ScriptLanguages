import math

import labs.lab7.src.functions as functions
import pytest


@pytest.mark.parametrize("strings,expected",
                         [(["zakład", "ubezpieczeń", "społecznych"], "ZUS"),
                         ([], "")])
def test_acronym(strings, expected):
    assert functions.acronym(strings) == expected


@pytest.mark.parametrize("nums,expected",
                         [([1, 1, 19, 2, 3, 4, 4, 5, 1], 3),
                          ([3, 4, 1, 5, 2, 6], 3.5)])
def test_median(nums, expected):
    assert functions.median(nums) == expected


@pytest.mark.parametrize("num,epsilon,expected",
                         [(3, 0.1, 1.75),
                          (2, 0.01, 1.417)])
def test_sqrt_newton(num, epsilon, expected):
    assert round(functions.sqrt_newton(num, epsilon), 3) == expected


@pytest.mark.parametrize("string,expected",
                         [("on i ona", {'o': ['on', 'ona'], 'n': ['on', 'ona'], 'i': ['i'], 'a': ['ona']}),
                          ("hello world", {'h': ['hello'], 'e': ['hello'], 'l': ['hello', 'world'], 'o': ['hello', 'world'], 'w': ['world'], 'd': ['world'], 'r': ['world']}),
                          ('to be, or not', {'t': ['to', 'not'],
                                             'e': ['be'],
                                             'o': ['to', 'or', 'not'],
                                             'b': ['be'],
                                             'r': ['or'],
                                             'n': ['not']})])
def test_make_alpha_dict(string,expected):
    assert functions.make_alpha_dict(string) == expected


@pytest.mark.parametrize("sequence,expected",
                         (
                             ([1, [2, 3], [[4, 5], 6]], [1, 2, 3, 4, 5, 6]),
                             ([[[2]], [3, 4], [[5], 6]], [2, 3, 4, 5, 6]),
                             (((1, 2), 4, (5, (6,))), [1, 2, 4, 5, 6])
                         ))
def test_flatten(sequence, expected):
    assert functions.flatten(sequence) == expected
