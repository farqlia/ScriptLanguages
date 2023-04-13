import argparse

# Tworzenie parsera argumentów
parser = argparse.ArgumentParser(description='Przykładowy program z podkomendami')

subparser1 = parser.add_subparsers(title='subcommand1', description='Podkomenda 1',
dest='subcommand1')
subparser1.add_parser('cmd1', help='Polecenie 1')

subparser2 = parser.add_subparsers(title='subcommand2', description='Podkomenda 2',
dest='subcommand2')
parser_cmd2 = subparser2.add_parser('cmd2', help='Polecenie 2')
parser_cmd2.add_argument('--arg', help='Opcjonalny argument')

print(parser.parse_args(['subcommand2', 'cmd2', '--arg', 'value']))