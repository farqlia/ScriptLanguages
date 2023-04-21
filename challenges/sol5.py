def solution(S):
    passwords = S.split(" ")
    print(passwords)

    longest_passwd = ""
    for password in passwords:
        if is_valid(password) and len(password) > len(longest_passwd):
            longest_passwd = password

    return len(longest_passwd)


def is_valid(passwd):
    n_digits = 0
    n_letters = 0
    for i in range(len(passwd)):
        if passwd[i].isdigit():
            n_digits += 1
        elif passwd[i].isalpha():
            n_letters += 1
        else:
            return False

    return n_digits % 2 == 1 and n_letters % 2 == 0


def test_1():
    print(solution('test 5 a0A pass007 ?xy1'))