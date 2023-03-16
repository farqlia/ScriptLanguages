'''What is a difference between a python module and a package?
A python module is a file with .py extension. A python package
consists of modules. When importing, everything is imported as
a module. When importing package however,
only variables/functions/classes defined in __init__.py
file are directly visible.
When importing a script, it is actually executed

If the interpreter runs the module, it's name will be
set to __main__. If it is executed from another module,
it's __name__ var will be set to that module's name
'''

import lectures.mypackage as pck
import lectures.mypackage.utils as u

print(pck.my_str)
u.funct()


class MyClass:
    pass


myclass = MyClass()
myclass.hello = "World"
print(myclass.hello)

x = 4


def print_x(x):
    print(x)
    x = 5
    print(x)


print_x(11)

_count = 0


def counter():
    # global identifiers means that the global variables
    # should be (re)bounded
    global _count
    _count = 16


counter()
print(_count)


def computation(a, b, c):
    print("performing computation")
    return a + b + c


def percent1(a, b, c):
    # the computations are performed only once
    def pc(x, total=computation(a, b, c)):
        return (x * 100.0) / total
    print("Percentages are: {:.2f}, {:.2f}, {:.2f}".format(pc(a), pc(b), pc(c)))


def percent2(a, b, c):
    def pc(x):
        # using local scope
        return (x * 100.0) / computation(a, b, c)
    print("Percentages are: {:.2f}, {:.2f}, {:.2f}".format(pc(a), pc(b), pc(c)))


percent1(1, 2, 3)
print()
percent2(1, 2, 3)

'''Function closure is a technique for binding names in some
environment (concept from functional programming)'''


