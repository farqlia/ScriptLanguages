def forall(pred, iterable):
    return sum([pred(elem) for elem in iterable]) == len(iterable)


def exists(pred, iterable):
    return sum([pred(elem) for elem in iterable]) >= 1


def atleast(n, pred, iterable):
    return sum([pred(elem) for elem in iterable]) >= n


def almost(n, pred, iterable):
    return sum([pred(elem) for elem in iterable]) <= n


