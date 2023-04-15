def solution(array, max_value):

    recovered = [-1 for _ in range(len(array))]

    i = 0
    while i < len(array) - 1:
        if array[i] != array[i + 1]:
            recovered[i] = array[i + 1]
        i += 1

    print(recovered)


def test_1():
    solution([0, 2, 2, 3, 7, 3], 10)
