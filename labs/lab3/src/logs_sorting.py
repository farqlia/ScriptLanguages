def sort_log(logs, key):

    if logs:
        if key < 0 or key > len(logs):
            raise IndexError("Key index out of bounds")

        sorted(logs, key=lambda l: l[key])

    return logs


