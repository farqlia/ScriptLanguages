def solution(countries_map):

    n_countries = 0
    N, M = len(countries_map), len(countries_map[0])

    def dfs(i, j, country):

        nonlocal countries_map
        countries_map[i][j] = None
        if is_valid(i - 1, j, N, M) and countries_map[i - 1][j] == country:
            dfs(i - 1, j, country)
        if is_valid(i + 1, j, N, M) and countries_map[i + 1][j] == country:
            dfs(i + 1, j, country)
        if is_valid(i, j + 1, N, M) and countries_map[i][j + 1] == country:
            dfs(i, j + 1, country)
        if is_valid(i, j - 1, N, M) and countries_map[i][j - 1] == country:
            dfs(i, j - 1, country)

    # convert to bfs because of recursion limit
    def bfs(country, queue):

        nonlocal countries_map
        countries_map[queue[0][0]][queue[0][1]] = None
        while queue:
            curr_len = len(queue)
            for _ in range(curr_len):
                i, j = queue.pop(0)
                if is_valid(i - 1, j, N, M) and countries_map[i - 1][j] == country:
                    countries_map[i - 1][j] = None
                    queue.append((i - 1, j))
                if is_valid(i + 1, j, N, M) and countries_map[i + 1][j] == country:
                    countries_map[i + 1][j] = None
                    queue.append((i + 1, j))
                if is_valid(i, j + 1, N, M) and countries_map[i][j + 1] == country:
                    countries_map[i][j + 1] = None
                    queue.append((i, j + 1))
                if is_valid(i, j - 1, N, M) and countries_map[i][j - 1] == country:
                    countries_map[i][j - 1] = None
                    queue.append((i, j - 1))

    for r in range(N):
        for c in range(M):
            if countries_map[r][c] is not None:
                n_countries += 1
                bfs(countries_map[r][c], [(r, c)])

    return n_countries


def is_valid(r, c, n, m):
    return r >= 0 and r < n and c >= 0 and c < m
