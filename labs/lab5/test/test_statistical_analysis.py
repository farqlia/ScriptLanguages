import math

import labs.lab5.src.statistical_analysis as statistical_analysis
import labs.lab5.src.ssh_logs_prepare as ssh_logs_prepare

import pytest
from pathlib import Path


@pytest.fixture
def one_user_entries():
    entries = []
    with open(Path.cwd().parent.joinpath('data', 'one_user.log')) as f:
        for line in f:
            entries.append(ssh_logs_prepare.parse_entry(line))
    return entries


def test_random_user(one_user_entries):
    print(statistical_analysis.get_random_user(one_user_entries))


def test_random_logs(one_user_entries):
    print(statistical_analysis.get_n_random_entries(one_user_entries, 3))


def test_connection_time(one_user_entries):
    assert statistical_analysis.compute_connection_time(one_user_entries) == {
        27952: 0.0, 27954: 2.0, 27956: 2.0
    }


def test_global_connection_times(one_user_entries):
    mean, std = statistical_analysis.global_connection_time(one_user_entries)
    assert mean == (4 / 3)
    assert std == math.sqrt(((2 - mean) ** 2 + (2 - mean) ** 2) / 2)


def test_user_connection_times(one_user_entries):
    print(statistical_analysis.user_connection_time(one_user_entries))
