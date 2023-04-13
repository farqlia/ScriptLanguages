import logging
import os.path
from pathlib import Path

import labs.lab5.src.regex_ssh_analysis as analyze_ssh_logs
import labs.lab5.src.statistical_analysis as statistical_analysis
import labs.lab5.src.ssh_logs_prepare as ssh_logs_prepare
import labs.lab5.src.logging_configure as logging_configure
import argparse


parser = argparse.ArgumentParser(description="SSH Logs Analyzer", add_help=True)

parser.add_argument('loc', help='location of the file')
parser.add_argument('-l', '--level', choices=['i', 'd', 'w', 'e', 'c'], required=False,
                    help='minimal logging level\ni - INFO, d - DEBUG, w - WARNING, e - ERROR, c - CRITICAL')

subparsers = parser.add_subparsers(title='Logs Analysis Commands', dest='functionality')

subparsers.add_parser('ipv4', help='Get all IPv4 addresses')
subparsers.add_parser('users', help='Get users')
subparsers.add_parser('mstype', help='Get message type')
nrand_parser = subparsers.add_parser('nrand', help='Get n random logs for a random user')
nrand_parser.add_argument('-n', type=int, default=1)
avg_parser = subparsers.add_parser('avg', help='Get average connection time')
avg_parser.add_argument('-s', '--scope', choices=['g', 'u'], default='g', help='g - global, u - for each user')
subparsers.add_parser('logfreq', help='Get most and least active user')

levels_dict = {
    'i': 'INFO', 'd': 'DEBUG', 'w': 'WARNING', 'e': 'ERROR', 'c': 'CRITICAL'
}


def exec_reg_commands(ssh_logs, arguments):

    f = lambda entry: entry

    if arguments.functionality == 'ipv4':
        f = lambda entry: f"IPv4 addresses: {analyze_ssh_logs.get_ipv4s_from_log(entry)}\n"
    elif arguments.functionality == 'users':
        f = lambda entry: f"Users: {analyze_ssh_logs.get_user_from_log(entry)}\n"
    elif arguments.functionality == 'mstype':
        f = lambda entry: f"Log type: {analyze_ssh_logs.get_message_type(entry)}"

    return [f(entry) for entry in ssh_logs]


def exec_stat_commands(ssh_logs, arguments):

    if arguments.functionality == 'nrand':
        return statistical_analysis.get_n_random_entries(ssh_logs, arguments.n)
    elif arguments.functionality == 'avg':
        if arguments.scope == 'u':
            return statistical_analysis.user_connection_time(ssh_logs)
        elif arguments.scope == 'g':
            return statistical_analysis.global_connection_time(ssh_logs)
    elif arguments.functionality == 'logfreq':
        return statistical_analysis.get_most_and_least_active(ssh_logs)

    return ""


def exec_commands(ssh_logs, arguments):

    if arguments.functionality == 'nrand':
        return "".format(statistical_analysis.get_n_random_entries(ssh_logs, arguments.n))
    elif arguments.functionality == 'avg':
        if arguments.scope == 'u':
            return [statistical_analysis.user_connection_time(ssh_logs)]
        elif arguments.scope == 'g':
            return [statistical_analysis.global_connection_time(ssh_logs)]
    elif arguments.functionality == 'logfreq':
        return statistical_analysis.get_most_and_least_active(ssh_logs)
    elif arguments.functionality == 'ipv4':
        return [f"IPv4 addresses: {analyze_ssh_logs.get_ipv4s_from_log(entry)}" for entry in ssh_logs]
    elif arguments.functionality == 'users':
        return [f"Users: {analyze_ssh_logs.get_user_from_log(entry)}" for entry in ssh_logs]
    elif arguments.functionality == 'mstype':
        return [f"Log type: {analyze_ssh_logs.get_message_type(entry)}" for entry in ssh_logs]

    return []


if __name__ == "__main__":
    args = parser.parse_args()
    file_location = args.loc

    if args.level:
        minimal_level = getattr(logging, levels_dict[args.level])
    else:
        minimal_level = logging.DEBUG

    if os.path.isfile(file_location):
        logging_configure.configure_logging(minimal_level)
        print(args)
        with open(file_location) as f:
            ssh_passed_logs = []

            for entry in f:
                ssh_passed_logs.append(ssh_logs_prepare.parse_entry(entry))
                logging_configure.log_data(ssh_passed_logs[-1])

            result = exec_commands(ssh_passed_logs, args)
            for r in result:
                print(r)

    else:
        print("Error: the file")