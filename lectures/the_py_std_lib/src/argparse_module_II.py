import argparse

# Subparsers allow you to split a command into many subcommands like git
# cam be invoked as git commit, git push etc.
parser = argparse.ArgumentParser("COCO")
parser.add_argument('--foo', action='store_true', help='foo help')
subparses = parser.add_subparsers(dest='subparser_name', help='sub-command help')

parser_a = subparses.add_parser('pa')
parser_a.add_argument('bar', type=int)

parser_b = subparses.add_parser('pb')
parser_b.add_argument('-b', '--baz', action='store_true')

print(parser.parse_args(['pa', '4']))
print(parser.parse_args(['--foo', 'pb', '-b']))