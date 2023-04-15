def solution(P, Q):
    # Implement your solution here
    P = list(P)
    Q = list(Q)
    return solve(P, Q, "")


def solve(P, Q, letter):

    solution_set = set()

    # What happens if we replace a letter with a given letter
    if letter != "":
        for i in range(len(P)):
            if P[i] == letter or Q[i] == letter:
                P[i] = letter
                Q[i] = letter
            P = [l for l in P if l != letter]
            Q = [l for l in Q if l != letter]

    for i in range(len(P)):
        solP = solve(P[i + 1:], Q[i + 1:], P[i])
        solQ = solve(P[i + 1:], Q[i + 1:], Q[i])

        if len(solution_set.union(solP)) <= len(solution_set.union(solQ)):
            solution_set.add(P[i])

    return solution_set


def solution2(P, Q):

    distinct_letters = set(P).union(set(Q))

    return solve2(P, Q, distinct_letters)


def solve2(P, Q, letters):

    if len(P) == 0:
        return set()

    min_set = set()

    for letter in letters:
        newP, newQ = replace_and_shrink(P, Q, letter)
        sol = solve2(newP, newQ, letters.difference({letter, })).union({letter, })
        if len(sol) < len(min_set) or not min_set:
            min_set = sol

    return min_set


def replace_and_shrink(P, Q, letter):

    newP, newQ = "", ""
    for i in range(len(P)):
        if P[i] != letter and Q[i] != letter:
            newP += P[i]
            newQ += Q[i]
    return newP, newQ


def test_sol1():
    print(solution2("abc", "bcd"))


def test_sol2():
    print(solution2("abada", "bacad"))

def test_sol3():
    print(solution2("amz", "amz"))


def test_sol4():
    print(solution2("axxz", "yzwy"))