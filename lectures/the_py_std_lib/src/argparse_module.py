import argparse

parser = argparse.ArgumentParser(description="Example program with arguments")

parser.add_argument('arg1', help='First positional argument')
parser.add_argument('--arg2', help='Second optional argument')
parser.add_argument('--arg3', help='Third optional req. argument')
parser.add_argument('-v', '--verbose', action='store_true', help='Turn on verbose mode')

args = parser.parse_args()

print(f"Arg 1: {args.arg1}")
if args.arg2:
    print(f"Arg 2: {args.arg2}")
print(f"Arg 3: {args.arg3}")

if args.verbose:
    print(f"Verbose mode turned on")