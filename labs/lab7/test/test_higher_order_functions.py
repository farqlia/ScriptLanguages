import labs.lab7.src.higher_order_functions as higher_order_functions
import pytest

@pytest.mark.parametrize("sequence,result",
                         [
                             ([1, 2, 3, 4, 5, 6, 7], True),
                             ([-1, 0, 1, 2], False),
                             ([0], False)
                         ])
def test_forall_are_greater_than_0(sequence, result):
    assert higher_order_functions.forall(lambda x: x > 0, sequence) == result


@pytest.mark.parametrize("sequence,result",
                         [
                             ([1, 2, 3, 4, 5, 6, 7], False),
                             ([-1, 0, 1, 2], True),
                             ([0], False)
                         ])
def test_exist_value_less_than_0(sequence, result):
    assert higher_order_functions.exists(lambda x: x < 0, sequence) == result


@pytest.mark.parametrize("sequence,n,result",
                         [
                             ([1, 2, 3, 4, 5, 6, 7], 7, True),
                             ([-2, -1, 0, 1], 1, True),
                             ([-2, -1, 0, 1, 2], 1, True),
                             ([0], 1, False)
                         ])
def test_atleast_n_values_greater_than_0(sequence, n, result):
    assert higher_order_functions.atleast(n, lambda x: x > 0, sequence) == result


@pytest.mark.parametrize("sequence,n,result",
                         [
                             ([1, 2, 3, 4, 5, 6, 7], 7, True),
                             ([1, 2, 3, 4, 5, 6, 7], 6, False),
                             ([-2, -1, 0, 1], 1, True),
                             ([-2, -1, 0, 1, 2], 1, False),
                             ([0], 1, True)
                         ])
def test_almost_n_values_greater_than_0(sequence, n, result):
    assert higher_order_functions.almost(n, lambda x: x > 0, sequence) == result
