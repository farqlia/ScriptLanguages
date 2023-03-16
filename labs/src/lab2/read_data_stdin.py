import sys

'''stdout and stderr are file-like objects that have write() method
which takes in string argument and stdin is a file-like object which
has readline() method that returns a line
In python we can make use of subtyping without inheritance
This is why we can implement only the functions we need in 
a given context '''


# lines = 10

for line in sys.stdin:
    print(line)
