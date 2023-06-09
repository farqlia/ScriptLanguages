import argparse
import logging
import os.path
import sys

import labs.ssh_logs_program.src.model.logging_configure as logging_module
import labs.ssh_logs_program.src.model.regex_ssh_utilis as analyze_ssh_logs
import labs.ssh_logs_program.src.model.ssh_logs_prepare as ssh_logs_prepare
import labs.ssh_logs_program.src.model.statistical_analysis as statistical_analysis


class Application:

    def __init__(self):

        self.parser = ssh_logs_prepare.Parser()

        self.levels_dict = {
            'i': 'INFO', 'd': 'DEBUG', 'w': 'WARNING', 'e': 'ERROR', 'c': 'CRITICAL'
        }
        self.arg_parser = argparse.ArgumentParser(description="SSH Logs Analyzer", add_help=True)

        self.arg_parser.add_argument('-n', '--nlines', type=int, help='max number of lines to read')
        self.arg_parser.add_argument('loc', help='location of the file')
        self.arg_parser.add_argument('-d', '--display', action='store_true', default=False, help='whether to display logs')
        self.arg_parser.add_argument('-l', '--level', choices=['i', 'd', 'w', 'e', 'c'], required=False,
                                      help='minimal logging level\ni - INFO, d - DEBUG, w - WARNING, e - ERROR, c - CRITICAL')

        self.arg_subparsers = self.arg_parser.add_subparsers(title='Logs Analysis Commands', dest='functionality')
        self.arg_subparsers.add_parser('ipv4', help='Get all IPv4 addresses')
        self.arg_subparsers.add_parser('users', help='Get users')
        self.arg_subparsers.add_parser('mstype', help='Get message type')
        self.nrand_parser = self.arg_subparsers.add_parser('nrand', help='Get n random logs for a random user')
        self.nrand_parser.add_argument('-n', type=int, default=1, help="Number of logs taken with replacement")
        self.avg_parser = self.arg_subparsers.add_parser('avg', help='Get average connection time')
        self.avg_parser.add_argument('-s', '--scope', choices=['g', 'u'], default='g', help='g - global, u - for each user')
        self.arg_subparsers.add_parser('logfreq', help='Get most and least active user')\

        self.results = None
        self.ssh_logs = []
        self.arguments = None

    def frmt(self, log):
        if self.arguments.display:
            return "\n" + self.parser.frmt(log)
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
            self.results = [f"User: {analyze_ssh_logs.get_user_from_log(entry)} {self.frmt(entry)}" for entry in self.ssh_logs]
        elif self.arguments.functionality == 'mstype':
            self.results = [f"Log type: {analyze_ssh_logs.get_message_type(entry).format()} {self.frmt(entry)}" for entry in self.ssh_logs]

    def _output_results(self):
        if isinstance(self.results, list):
            for row in self.results:
                print(row)
        elif isinstance(self.results, dict):
            for k, v in self.results.items():
                print(f"{k}: {v}")
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

                n_lines = 0
                for entry in f:
                    try:
                        self.ssh_logs.append(self.parser.parse_entry(entry))
                        self.log_data(self.ssh_logs[-1])
                    except ValueError as e:
                        logging.error(e)

                    n_lines += 1
                    if self.arguments.nlines and n_lines == self.arguments.nlines:
                        break
            return True
        else:
            sys.stderr.write(f"Error: the file {file_location} does not exist")
            return False

    def run(self):

        self.arguments = self.arg_parser.parse_args()
        # print(self.arguments)

        self._configure_logging()

        if self.read_data():
            self._exec_commands()
            self._output_results()


if __name__ == "__main__":

    App = Application()
    App.run()