import math


def solution(X, Y, colors):
    # Implement your solution here
    points = list(zip(X, Y))

    points_red = sorted([points[i] for i in range(len(X)) if colors[i] == 'R'], key=lambda p: distance(p))
    points_green = sorted([points[i] for i in range(len(X)) if colors[i] == 'G'], key=lambda p: distance(p))



    n_red_points = 0
    n_green_points = 0

    n_if_feasible = 0

    max_radius = max(distance(points_red[-1]), distance(points_green[-1]))

    while n_red_points < len(points_red) or n_green_points < len(points_green):
        radius = min(distance(points_red[n_red_points]) if n_red_points < len(points_red) else max_radius,
                     distance(points_green[n_green_points]) if n_green_points < len(points_green) else max_radius)
        while n_red_points < len(points_red) and distance(points_red[n_red_points]) <= radius:
            n_red_points += 1
        while n_green_points < len(points_green) and distance(points_green[n_green_points]) <= radius:
            n_green_points += 1

        if n_red_points == n_green_points:
            n_if_feasible = n_red_points

    return 2 * n_if_feasible


def distance(p):
    return math.sqrt(p[0] ** 2 + p[1] ** 2)


def test_1():
    X = [4, 0, 2, -2]
    Y = [4, 1, 2, -3]
    colors = list('RGRR')
    assert solution(X, Y, colors) == 2


def test_2():
    X = [1, 1, -1, -1]
    Y = [1, -1, 1, -1]
    colors = list('RGRG')
    assert solution(X, Y, colors) == 4


def test_3():
    X = [1, 0, 0]
    Y = [0, 1, -1]
    colors = list('GGR')
    assert solution(X, Y, colors) == 0


def test_4():
    X = [5, -5, 5]
    Y = [1, -1, 3]
    colors = list('GRG')
    assert solution(X, Y, colors) == 2


def test_5():
    X = [3000, -3000, 4100, -4100, -3000]
    Y = [5000, -5000, 4100, -4100, 5000]
    colors = list('RRGRG')
    assert solution(X, Y, colors) == 2

