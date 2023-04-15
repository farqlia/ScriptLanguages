def solution(A):

    B = [-1 for _ in range(len(A) + 2)]

    for n in A:
        if 0 < n < len(B):
            B[n] = n

    i = 1
    while B[i] != -1:
        i += 1

    return i