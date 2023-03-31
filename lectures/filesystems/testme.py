import pathlib

# This is the directory from where the script is run
print(pathlib.Path.cwd())
# Directory where the file resides
print(pathlib.Path(__file__).parent)