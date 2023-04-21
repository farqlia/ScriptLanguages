def solution(H):
    # Implement your solution here

    stack = []
    n_blocks = 0

    for h in H:

        while stack and stack[-1] >= h:
            if stack[-1] != h:
                n_blocks += 1
            stack.pop()

        stack.append(h)
        print("s: ", stack)

    while len(stack) > 1:
        if stack[0] != stack[1]:
            n_blocks += 1
        stack.pop()

    n_blocks += 1

    return n_blocks


def test_1():
    print(solution([8, 8, 5, 7, 9, 8, 7, 4, 8]))

def test_2():
    print(solution([1, 2, 3, 4, 5, 6, 7, 8]))