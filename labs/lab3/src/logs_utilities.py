import labs.lab3.src.logs_reader as lr
from functools import partial


def sort_log(logs, key):

    if not logs or key < 0 or key > len(logs[0]):
        raise IndexError("Key index out of bounds")

    logs = sorted(logs, key=lambda l: l[key])

    return logs


def is_response_code_valid(code):
    return 100 <= code <= 599


def is_entry_response_code_valid(log):
    return is_response_code_valid(log[lr.STATUS_CODE_INDEX])


def filter_logs(logs, *predicates):

    filtered = [log for log in logs if all(predicate(log) for predicate in predicates)]

    return filtered


def is_resource(log, resource):
    return log[lr.HOSTNAME_INDEX] == resource


def get_entries_by_addr(resource, log):

    return filter_logs(log,
                       # is_log_response_code_valid,
                       partial(is_resource, resource=resource))


def has_response_code(log, code):
    return log[lr.STATUS_CODE_INDEX] == code


def get_entries_by_code(code, log):
    return filter_logs(log, partial(has_response_code, code=code)) if is_response_code_valid(code) else []


def is_response_code_type(log, code_prefix):

    return log[lr.STATUS_CODE_INDEX] // 100 == code_prefix


def get_failed_reads(log, merged=True):

    is_4xx = partial(is_response_code_type, code_prefix=4)
    is_5xx = partial(is_response_code_type, code_prefix=5)

    failed_4xx_reads = filter_logs(log, is_4xx)
    failed_5xx_reads = filter_logs(log, is_5xx)

    if merged:
        failed_reads = failed_4xx_reads + failed_5xx_reads
    else:
        failed_reads = failed_4xx_reads, failed_5xx_reads

    return failed_reads


def is_of_extension(log, extension):
    return log[lr.RESOURCE_PATH_INDEX].endswith('.' + extension)


# Many extensions?
def get_entries_by_extension(log, extension):
    return filter_logs(log, partial(is_of_extension, extension=extension))


def print_entries(log):
    for entry in log:
        print(entry)


def get_addrs(logs):
    return list(logs.keys()) if isinstance(logs, dict) else []


def string_dict_entry_dates(key, list_of_host_log):

    n = len(list_of_host_log)
    logs_200_fraction = len(get_entries_by_code(200, list_of_host_log)) / n

    by_date = lambda l: l[lr.DATE_INDEX]
    oldest_entry = min(list_of_host_log, key=by_date)
    recent_entry = max(list_of_host_log, key=by_date)

    date_format = "%d/%m/%Y"

    info = f"{key} sent {n} queries between {by_date(oldest_entry).strftime(date_format)} and " \
           f"{by_date(recent_entry).strftime(date_format)} with {round(logs_200_fraction, 2) * 100}% successful responses."

    return info


def print_dict_entry_dates(log):
    if isinstance(log, dict):
        for k, v in log.items():
            print(string_dict_entry_dates(k, v))

