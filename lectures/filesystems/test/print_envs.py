import os
import sys

script_path = sys.argv[0]

print(script_path)

print(os.getcwd())
print()

for var in sys.argv[1:]:
    print(var)

