import sys
def funct():
    print(f"Hello World, my name is {__name__}")

if __name__ == '__main__':
    print("I'm executed directly")
    funct()

else:
    print("I'm being imported")