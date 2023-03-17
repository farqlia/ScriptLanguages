import sys

n = len(sys.argv)

print(sys.argv[0])

print("Arguments Passed: ")
for i in range(1, n):
    print(sys.argv[i])