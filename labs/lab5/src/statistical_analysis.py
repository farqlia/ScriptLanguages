import labs.lab5.src.regex_ssh_analysis as regex_ssh_analysis
from collections import Counter

import random
import statistics


def get_random_user(users):

    while True:
        user = random.choice(users)
        if user:
            return user


def get_n_random_entries(ssh_logs, n):

    users = [regex_ssh_analysis.get_user_from_log(entry) for entry in ssh_logs]
    rand_usr = get_random_user(users)
    return random.choices(list(map(lambda e: e[0],
                          filter(lambda e: e[1] == rand_usr, zip(ssh_logs, users)))), k=n)


def compute_connection_time(ssh_logs):
    open_connection_time = {}
    connection_time = {}
    for entry in ssh_logs:

        user = regex_ssh_analysis.get_user_from_log(entry)
        ipv4_address = regex_ssh_analysis.get_ipv4s_from_log(entry)

        if regex_ssh_analysis.get_message_type(entry) == regex_ssh_analysis.MessageType.UNSUCCESSFUL_LOGIN and ipv4_address and user:
            open_connection_time[ipv4_address[0]] = (entry.date, user)

        elif ipv4_address and ipv4_address[0] in open_connection_time and \
                regex_ssh_analysis.get_message_type(entry) == regex_ssh_analysis.MessageType.CLOSED_CONNECTION:
            connection_date, user = open_connection_time[ipv4_address[0]]
            connection_time[user] = connection_time.get(user, 0) + (
                    entry.date - connection_date).total_seconds()

    return connection_time


def compute_connection_time2(ssh_logs):

    connection_time = {}
    for i, entry in enumerate(ssh_logs):

        user = regex_ssh_analysis.get_user_from_log(entry)
        ipv4_address = regex_ssh_analysis.get_ipv4s_from_log(entry)

        if regex_ssh_analysis.get_message_type(entry) == regex_ssh_analysis.MessageType.UNSUCCESSFUL_LOGIN\
                and ipv4_address:

            for j in range(i + 1, len(ssh_logs)):
                if regex_ssh_analysis.get_message_type(ssh_logs[j]) == regex_ssh_analysis.MessageType.CLOSED_CONNECTION\
                        and ipv4_address == regex_ssh_analysis.get_ipv4s_from_log(ssh_logs[j]):
                    connection_time[user] = connection_time.get(user, 0) + (
                            ssh_logs[j].date - entry.date).total_seconds()

    return connection_time


def global_connection_time(ssh_logs):
    connection_times = compute_connection_time(ssh_logs)
    return statistics.mean(connection_times.values()), statistics.stdev(connection_times.values())


def user_connection_time(ssh_logs):
    connection_times = compute_connection_time(ssh_logs)
    users_connection_times = {}

    for entry in ssh_logs:
        user = regex_ssh_analysis.get_user_from_log(entry)
        if user and (entry.pid in connection_times):
            if user not in users_connection_times:
                users_connection_times[user] = []
            users_connection_times[user].append(connection_times[entry.pid])

    return {k: (statistics.mean(v), statistics.stdev(v) if len(v) > 1 else 0) for k, v in users_connection_times.items()}


def get_most_and_least_active(ssh_logs):
    users = list(filter(lambda u: u is not None, (regex_ssh_analysis.get_user_from_log(entry) for entry in ssh_logs)))
    counter = Counter(users)
    return counter.most_common(1)[0][0], counter.most_common()[-1][0]




