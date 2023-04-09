import argparse

# Subparsers allow you to split a command into many subcommands like git
# cam be invoked as git commit, git push etc.
parser = argparse.ArgumentParser("COCO")
parser.add_argument('--foo', action='store_true', help='foo help')
subparses = parser.add_subparsers(help='sub-command help')

parser_a = subparses.add_parser('a')
parser_a.add_argument('bar', type=int)

parser_b = subparses.add_parser('b')
parser_b.add_argument('--baz', choices='XYZ')

print(parser.parse_args(['a', '12']))
print(parser.parse_args(['--foo', 'b', '--baz', 'Z']))