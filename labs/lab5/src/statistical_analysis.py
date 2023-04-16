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


def compute_user_connection_times(ssh_logs):

    connection_time = {}

    for i, entry in enumerate(ssh_logs):

        user = regex_ssh_analysis.get_user_from_log(entry)
        ipv4_address = regex_ssh_analysis.get_ipv4s_from_log(entry)

        if user not in connection_time:
            connection_time[user] = []

        if regex_ssh_analysis.get_message_type(entry) == regex_ssh_analysis.MessageType.CLOSED_CONNECTION and ipv4_address:

            for j in range(i - 1, 0, -1):

                this_ipv4 = regex_ssh_analysis.get_ipv4s_from_log(ssh_logs[j])
                user = regex_ssh_analysis.get_user_from_log(ssh_logs[j])

                mstype = regex_ssh_analysis.get_message_type(ssh_logs[j])
                if (mstype == regex_ssh_analysis.MessageType.UNSUCCESSFUL_LOGIN
                or mstype == regex_ssh_analysis.MessageType.INCORRECT_USERNAME) and ipv4_address == this_ipv4\
                        and user:
                    connection_time[user].append((entry.date - ssh_logs[j].date).total_seconds())
                    break

    return connection_time


def global_connection_time(ssh_logs):
    connection_times = compute_user_connection_times(ssh_logs)
    all_values = [time for times in connection_times.values() for time in times]
    return statistics.mean(all_values) if len(all_values) > 0 else 0,\
           statistics.stdev(all_values) if len(all_values) > 1 else 0


def user_connection_time(ssh_logs):
    connection_times = compute_user_connection_times(ssh_logs)
    return {k: (statistics.mean(v) if len(v) > 0 else 0, statistics.stdev(v) if len(v) > 1 else 0)
            for k, v in connection_times.items()}


def get_most_and_least_active(ssh_logs):
    users = list(filter(lambda u: u is not None, (regex_ssh_analysis.get_user_from_log(entry) for entry in ssh_logs)))
    counter = Counter(users)
    return counter.most_common(1)[0][0], counter.most_common()[-1][0]




