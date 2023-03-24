import sys

'''stdout and stderr are file-like objects that have write() method
which takes in string argument and stdin is a file-like object which
has readline() method that returns a line
In python we can make use of subtyping without inheritance
This is why we can implement only the functions we need in 
a given context '''


def read_lines():

    if len(sys.argv) > 1 and sys.argv[1].isdigit():
        lines = int(sys.argv[1])
    else:
        lines = 0

    if lines > 0:
        for _ in range(lines):
            print(sys.stdin.readline().rstrip())

    else:
        for line in sys.stdin:
            print(line.rstrip())


if __name__ == '__main__':

    read_lines()




