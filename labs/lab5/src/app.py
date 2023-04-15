import logging
import os.path
from pathlib import Path

import labs.lab5.src.regex_ssh_analysis as analyze_ssh_logs
import labs.lab5.src.statistical_analysis as statistical_analysis
import labs.lab5.src.ssh_logs_prepare as ssh_logs_prepare
import labs.lab5.src.logging_configure as logging_module
import argparse


class Application:

    def __init__(self):

        self.levels_dict = {
            'i': 'INFO', 'd': 'DEBUG', 'w': 'WARNING', 'e': 'ERROR', 'c': 'CRITICAL'
        }
        self.parser = argparse.ArgumentParser(description="SSH Logs Analyzer", add_help=True)

        self.parser.add_argument('loc', help='location of the file')
        self.parser.add_argument('-d', '--display', action='store_true', default=False, help='whether to display logs')
        self.parser.add_argument('-l', '--level', choices=['i', 'd', 'w', 'e', 'c'], required=False,
                            help='minimal logging level\ni - INFO, d - DEBUG, w - WARNING, e - ERROR, c - CRITICAL')

        self.subparsers = self.parser.add_subparsers(title='Logs Analysis Commands', dest='functionality')
        self.subparsers.add_parser('ipv4', help='Get all IPv4 addresses')
        self.subparsers.add_parser('users', help='Get users')
        self.subparsers.add_parser('mstype', help='Get message type')
        self.nrand_parser = self.subparsers.add_parser('nrand', help='Get n random logs for a random user')
        self.nrand_parser.add_argument('-n', type=int, default=1)
        self.avg_parser = self.subparsers.add_parser('avg', help='Get average connection time')
        self.avg_parser.add_argument('-s', '--scope', choices=['g', 'u'], default='g', help='g - global, u - for each user')
        self.subparsers.add_parser('logfreq', help='Get most and least active user')\

        self.results = None
        self.ssh_logs = []
        self.arguments = None

    def frmt(self, log):
        if self.arguments.display:
            return ", '" + log.message[:30] + " [...]'"
        else:
            return ""

    def _exec_commands(self):

        if self.arguments.functionality == 'nrand':
            self.results = statistical_analysis.get_n_random_entries(self.ssh_logs, self.arguments.n)
        elif self.arguments.functionality == 'avg':
            if self.arguments.scope == 'u':
                self.results = statistical_analysis.user_connection_time(self.ssh_logs)
            elif self.arguments.scope == 'g':
                self.results = statistical_analysis.global_connection_time(self.ssh_logs)
        elif self.arguments.functionality == 'logfreq':
            self.results = statistical_analysis.get_most_and_least_active(self.ssh_logs)
        elif self.arguments.functionality == 'ipv4':
            self.results = [f"IPv4 addresses: {analyze_ssh_logs.get_ipv4s_from_log(entry)} {self.frmt(entry)}" for entry in self.ssh_logs]
        elif self.arguments.functionality == 'users':
            self.results = [f"Users: {analyze_ssh_logs.get_user_from_log(entry)} {self.frmt(entry)}" for entry in self.ssh_logs]
        elif self.arguments.functionality == 'mstype':
            self.results = [f"Log type: {analyze_ssh_logs.get_message_type(entry)} {self.frmt(entry)}" for entry in self.ssh_logs]

    def _output_results(self):
        if isinstance(self.results, list):
            for row in self.results:
                print(row)
        else:
            if self.results:
                print(self.results)

    def _configure_logging(self):
        if self.arguments.level:
            minimal_level = getattr(logging, self.levels_dict[self.arguments.level])
            logging_module.configure_logging(minimal_level)

    def log_data(self, data):
        if self.arguments.level:
            logging_module.log_data(data, self.arguments.display)

    def log_error(self, msg):
        if self.arguments.level:
            logging.error(msg)

    def read_data(self):
        file_location = self.arguments.loc
        if os.path.isfile(file_location):
            with open(file_location) as f:

                for entry in f:
                    try:
                        self.ssh_logs.append(ssh_logs_prepare.parse_entry(entry))
                        self.log_data(self.ssh_logs[-1])
                    except ValueError as e:
                        logging.error(e)

            return True
        else:
            logging.error(f"Error: the file {file_location} does not exist")
            return False

    def run(self):

        self.arguments = self.parser.parse_args()
        print(self.arguments)

        self._configure_logging()

        if self.read_data():
            self._exec_commands()
            self._output_results()


if __name__ == "__main__":

    App = Application()
    App.run()