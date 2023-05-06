def n_of_true_elements(pred, iterable):
    return sum([pred(elem) for elem in iterable])


def forall(pred, iterable):
    return n_of_true_elements(pred, iterable) == len(iterable)


def exists(pred, iterable):
    return n_of_true_elements(pred, iterable) >= 1


def atleast(n, pred, iterable):
    return n_of_true_elements(pred, iterable) >= n


def almost(n, pred, iterable):
    return n_of_true_elements(pred, iterable) <= n


