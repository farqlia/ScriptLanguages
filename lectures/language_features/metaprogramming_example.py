import inspect
import dis
from collections.abc import Iterable, Iterator
from abc import ABCMeta

def generate_program(numbers):
    program_code = f'''
def calculate_sum():
    numbers = {numbers}
    total = sum(numbers)
    print("Sum of numbers: ", total)
    
calculate_sum()
'''

    with open('generated_program.py', 'w') as f:
        f.write(program_code)


class B:

    def __init__(self):
        self.name = 'example class'
        self.value = 1984


def make_person(attrs, env):
    attr_str = "\n".join([f"\t{n}:{t}" for t in attrs.keys() for n in attrs[t]])
    exec(f"""
from dataclasses import dataclass
@dataclass
class Person:
{attr_str}
""", None, env)


def four():
    a = 1
    while a < 4:
        a += 1
    print(a)


if __name__ == "__main__":
    numbers = [1, 2, 3, 4, 5]
    generate_program(numbers)

    print(dir(B()))
    print(dir(1))

    print(inspect.isclass(B))
    print(inspect.isbuiltin(sum))
    print(inspect.isfunction(generate_program))

    print(inspect.getmembers(B()))

    print(inspect.getsource(B))

    code = 'print("hello world")'
    exec(code)

    attrs = {
        'int': ['weight', 'height'],
        'str': ['name', 'surname']
    }

    make_person(attrs, locals())

    person = Person(height=175, weight=66, name='John', surname='Doe')
    print(person)

    # eval is similar to exec() but it returns the result
    # of computation
    print(eval("2 + 2"))
    print(eval("isinstance(4, int)"))

    dis.dis(four)

    # type called this way returns the type of an object
    print(type(sum))

    # Other functionality of type is to create classes
    # at runtime
    # This way type is a metaclass - a class used
    # to build classes
    MyClass = type('MyClass',
                    (Iterable, B),
                    {'x': 42, 'x2': lambda self: self.x * 2,
                     '__iter__': lambda self: None})

    my_class = MyClass()
    print(my_class.x2())

    print(Iterable.__class__)
    # All classes are instances of type, but only metaclasses are subclasses of type
    # This way they inherit power to construct classes
    print(ABCMeta.__class__)
