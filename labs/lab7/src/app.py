import time

from log_decorator import log
import typing
import logging
import password_generator
import closures
import timeit


@log(logging.DEBUG)
class Duck:

    def __init__(self, name: str, age: int, fav_food: typing.List[str]):
        self.name = name
        self.age = age
        self.fav_food = fav_food
        time.sleep(0.5)

    def quack(self):
        return "quack"


@log(logging.WARNING)
def kill_ducks(ducks: typing.List[Duck], n_tortures=999):
    for duck in ducks:
        for _ in range(n_tortures):
            duck.quack()

    return len(ducks)


if __name__ == "__main__":

    psswd_gen = password_generator.PasswordGenerator(length=10, count=5)

    print("Iterate with for")
    for passwd in psswd_gen:
        print("Password: ", passwd)

    passwd_iter = iter(psswd_gen)
    print("Iterate with next()")
    print("Password: ", next(passwd_iter))
    print("Password: ", next(passwd_iter))
    print("Password: ", next(passwd_iter))
    print("Password: ", next(passwd_iter))
    print("Password: ", next(passwd_iter))

    try:
        next(passwd_iter)
    except StopIteration:
        print("Generated all passwords")

    fib_gen = closures.make_generator(closures.fibonacci)
    for _ in range(10):
        print(fib_gen())

    # TODO : implement with memoization
    fib_gen_memo = closures.make_generator_mem(closures.fibonacci)
    gen = fib_gen_memo()
    # print(timeit.timeit('[fib_gen_memo() for _ in range(20)]', number=1, globals=globals()))
    # print(timeit.timeit('[fib_gen_memo() for _ in range(20)]', number=1, globals=globals()))

    print(timeit.Timer('for _ in range(40): gen()', globals=globals()).timeit(number=1))
    gen = fib_gen_memo()
    print(timeit.Timer('for _ in range(40): gen()', globals=globals()).timeit(number=1))

    ducks = [Duck("John", 1, ["Carrot", "Bread"]), Duck("Tom", 4, ["Pea"])]

    kill_ducks(ducks)

