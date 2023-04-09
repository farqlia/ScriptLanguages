import re
import pytest


@pytest.mark.parametrize("string,expected",
                         [("First Name and Last name: Marylin Monroe", "Marylin Monroe"),
                          ("Name: Marylin Monroe", None)])
def test_lookbehind_assertion(string, expected):
    pattern = r"(?<=First Name and Last name:\s)[A-Z][a-z]+\s[A-Z][a-z]+"
    match = re.search(pattern, "")
    assert match.match == expected if match else not expected


@pytest.mark.parametrize("string,expected",
                         [("word.txt", "word"),
                          ("photo.jpg", None)])
def test_lookahead_assertion(string, expected):
    pattern = "\w+(?=\.txt)"
    match = re.search(pattern, "")
    assert match.match == expected if match else not expected


@pytest.mark.parametrize("string,expected_groups",
                         [("ho hohoho", ("ho", "hoho"))])
def test_groups(string, expected_groups):
    pattern = r"([a-zA-Z]+)\s\1(\1\1)"
    match = re.match(pattern, string)
    print(match.groups())
    assert match.groups() == expected_groups if match else not expected_groups
