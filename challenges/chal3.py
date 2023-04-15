def solution(S):

    # Skip trailing zeros
    while S[0] == '0':
        S = S[1:]

    i = 0
    while len(S) > 1:
        if S[-1] == '0':
            i += 1
        else:
            i += 2
        S = S[:-1]

    # the subtraction of 1
    return i + 1


def test_1():
    assert solution("011100") == 7
    assert solution("111") == 5
    assert solution("1111010101111") == 22
    assert solution(400_000 * "1") == 799_999
