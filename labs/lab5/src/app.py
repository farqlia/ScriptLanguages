import logging
import os.path
from pathlib import Path

import labs.lab5.src.regex_ssh_analysis as analyze_ssh_logs
import labs.lab5.src.logging_configure as logging_configure
import argparse


parser = argparse.ArgumentParser(description="SSH Logs Analyzer", add_help=True)

parser.add_argument('loc', help='location of the file')
parser.add_argument('--level', choices=['i', 'd', 'w', 'e', 'c'], required=False,
                    help='minimal logging level\ni - INFO, d - DEBUG, w - WARNING, e - ERROR, c - CRITICAL')

subparsers = parser.add_subparsers(title='Logs Analysis Commands', dest='subcommand2')

parser_reg = subparsers.add_parser('reg', help='Regular expression analysis')
parser_reg.add_argument('-i', '--ipv4', action='store_true', default=False, help='Get all IPv4 addresses')
parser_reg.add_argument('-u', '--users', action='store_true',  help='Get users')
parser_reg.add_argument('-t', '--mstype', action='store_true', help='Get message type')


parse_stat = subparsers.add_parser('stat', help='Statistical Analysis')
parse_stat.add_argument('-r', '--nrand', action='store_true', default=False)
parse_stat.add_argument('-a', '--avgglob', choices=['global', 'users'], default='global')
parse_stat.add_argument('-f', '--logfreq', action='store_true', default=False)

levels_dict = {
    'i': 'INFO', 'd': 'DEBUG', 'w': 'WARNING', 'e': 'ERROR', 'c': 'CRITICAL'
}


def exec_reg_commands(log_entry, arguments):

    command_output = ""

    if arguments.ipv4:
        command_output += f"IPv4 addresses: {analyze_ssh_logs.get_ipv4s_from_log(log_entry)}\n"
    if arguments.users:
        command_output += f"Users: {analyze_ssh_logs.get_user_from_log(log_entry)}\n"
    if arguments.mstype:
        command_output += f"Log type: {analyze_ssh_logs.get_message_type(log_entry)}"

    return command_output.strip()


def exec_stat_commands(log_entry, arguments):
    return ""


def exec_commands(log_entry, arguments):

    command_output = "Analyze: " + (" ".join(map(str, log_entry))) + "\n"

    if arguments.subcommand == 'reg':
        command_output += exec_reg_commands(log_entry, arguments)
    elif arguments.subcommand == 'stat':
        command_output += exec_stat_commands('stat', arguments)

    return command_output


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
            for line in f:
                log_entry_instance = analyze_ssh_logs.parse_entry(line)
                logging_configure.log_entry_type(log_entry_instance)
                print(exec_commands(log_entry_instance, args))
    else:
        print("Error: the file")