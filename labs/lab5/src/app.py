import logging
import os.path
from pathlib import Path

import labs.lab5.src.analyze_ssh_logs as analyze_ssh_logs
import labs.lab5.src.logging_configure as logging_configure
import argparse


parser = argparse.ArgumentParser(description="SSH Logs Analyzer")

parser.add_argument('loc', help='location of the file')
parser.add_argument('--level', choices=['i', 'd', 'w', 'e', 'c'], required=False,
                    help='minimal logging level\ni - INFO, d - DEBUG, w - WARNING, e - ERROR, c - CRITICAL')

subparsers = parser.add_subparsers()

parser_reg = subparsers.add_parser('reg', help='Regular expression analysis')
parser_reg.add_argument('-i', '--ipv4', action='store_true', default=False, help='Get all IPv4 addresses')
parser_reg.add_argument('-u', '--users', action='store_true',  help='Get users')
parser_reg.add_argument('-t', '--mstype', action='store_true', help='Get message type')

levels_dict = {
    'i': 'INFO', 'd': 'DEBUG', 'w': 'WARNING', 'e': 'ERROR', 'c': 'CRITICAL'
}


def exec_commands(log_entry, arguments):

    command_output = "Analyze: " + (" ".join(map(str, log_entry))) + "\n"

    if arguments.ipv4:
        command_output += f"IPv4 addresses: {analyze_ssh_logs.get_ipv4s_from_log(log_entry)}\n"
    if arguments.users:
        command_output += f"Users: {analyze_ssh_logs.get_user_from_log(log_entry)}\n"
    if arguments.mstype:
        command_output += f"Log type: {analyze_ssh_logs.get_message_type(log_entry)}"

    return command_output.strip()


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