import labs.lab3.src.logs_reader as lr
from functools import partial


def sort_log(logs, key):

    if logs:
        if key < 0 or key > len(logs[0]):
            raise IndexError("Key index out of bounds")

        logs = sorted(logs, key=lambda l: l[key])

    return logs


def filter_logs(logs, *predicates):

    filtered = [log for log in logs if all(predicate(log) for predicate in predicates)]

    return filtered


def get_entries_by_addr(resource, logs):

    def is_resource(log):
        return log[lr.HOSTNAME_INDEX] == resource

    return filter_logs(logs, partial(is_response_code_type, code_prefix=2), is_resource)


def is_response_code_valid(code):

    return 100 <= code <= 599


def has_response_code(log, code):
    return log[lr.RESPONSE_CODE_INDEX] == code


def get_entries_by_code(code, logs):

    return filter_logs(logs, partial(has_response_code, code=code)) if is_response_code_valid(code) else []


def split_on_condition(_list, predicate):

    split_list = ([], [])
    for elem in _list:
        if predicate(elem):
            split_list[0].append(elem)
        else:
            split_list[1].append(elem)

    return split_list


def is_response_code_type(log, code_prefix):

    return log[lr.RESPONSE_CODE_INDEX] // 100 == code_prefix


def get_failed_reads(logs, merged=True):

    is_4xx = partial(is_response_code_type, code_prefix=4)
    is_5xx = partial(is_response_code_type, code_prefix=5)

    failed_reads = filter_logs(logs, lambda l: is_4xx(l) or is_5xx(l))

    if not merged:
        failed_reads = split_on_condition(failed_reads, is_4xx)

    return failed_reads

