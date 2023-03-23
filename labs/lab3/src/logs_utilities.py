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


def is_resource(log, resource):
    return log[lr.HOSTNAME_INDEX] == resource


def get_entries_by_addr(resource, logs):

    return filter_logs(logs,
                       # partial(is_response_code_type, code_prefix=2), ???????

                       partial(is_resource, resource=resource))


def is_response_code_valid(code):

    return 100 <= code <= 599


def has_response_code(log, code):
    return log[lr.STATUS_CODE_INDEX] == code


def get_entries_by_code(code, logs):

    return filter_logs(logs, partial(has_response_code, code=code)) if is_response_code_valid(code) else []


def is_response_code_type(log, code_prefix):

    return log[lr.STATUS_CODE_INDEX] // 100 == code_prefix


def get_failed_reads(logs, merged=True):

    is_4xx = partial(is_response_code_type, code_prefix=4)
    is_5xx = partial(is_response_code_type, code_prefix=5)

    failed_4xx_reads = filter_logs(logs, is_4xx)
    failed_5xx_reads = filter_logs(logs, is_5xx)

    if merged:
        failed_reads = failed_4xx_reads + failed_5xx_reads
    else:
        failed_reads = failed_4xx_reads, failed_5xx_reads

    return failed_reads


def get_entries_by_extension(logs, *extensions):

    def is_of_extension(log):
        return any(log[lr.RESOURCE_PATH_INDEX].endswith('.' + ext) for ext in extensions)

    return filter_logs(logs, is_of_extension)


def print_entries(logs):

    for log in logs:
        print(log)


def get_addrs(logs):
    return logs.keys() if isinstance(logs, dict) else []


def string_dict_entry_dates(key, list_of_host_logs):

    n = len(list_of_host_logs)
    logs_200_fraction = len(get_entries_by_code(200, list_of_host_logs)) / n
    sorted_by_date = sort_log(list_of_host_logs, lr.DATE_INDEX)
    date_format = "%d/%m/%Y"

    info = f"{key} sent {n} queries between {sorted_by_date[0][lr.DATE_INDEX].strftime(date_format)} and " \
           f"{sorted_by_date[-1][lr.DATE_INDEX].strftime(date_format)} with {round(logs_200_fraction, 2) * 100}% successful responses."

    return info


def print_dict_entry_dates(logs):
    if isinstance(logs, dict):
        for k, v in logs.items():
            print(string_dict_entry_dates(k, v))

