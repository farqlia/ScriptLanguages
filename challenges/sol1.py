
def solution(S):

    sum_of_digits = sum([int(S[i]) for i in range(len(S))])

    possible_numbers = 0

    positive_increment = 3 - (sum_of_digits % 3)
    negative_increment = (sum_of_digits % 3)

    if negative_increment == 0:
        possible_numbers = 1 - len(S)

    for i in range(len(S)):

        digit = int(S[i])

        # Round to the nearest greater value div by 3
        digit += positive_increment
        possible_numbers += (9 - digit) // 3 + 1

        digit -= (positive_increment + negative_increment)
        possible_numbers += digit // 3 + 1

    return possible_numbers


def test_1():
    print(solution("23"))

def test_2():
    print(solution("0081"))

def test_3():
    print(solution("022"))
