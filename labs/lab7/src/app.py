import time

from labs.lab7.src.log_decorator import log
import typing
import logging
import labs.lab7.src.password_generator
import closures
import timeit


@log(logging.DEBUG)
class Duck:

    def __init__(self, name: str, age: int, fav_food: typing.List[str]):
        self.name = name
        self.age = age
        self.fav_food = fav_food
        # hatching
        time.sleep(0.5)

    def set_friend(self, friend: "Duck"):
        self.friend = friend
        friend.friend = self

    def set_quack(self, quack: typing.Callable[[], None]):
        self._quack = quack

    def quack(self):
        self._quack()


@log(logging.WARNING)
def kill_ducks(ducks: typing.List[Duck], n_tortures=999):
    for duck in ducks:
        for _ in range(n_tortures):
            duck.quack()

    return len(ducks)


@log(logging.INFO)
def generate_fibs_up_to(n, generator):
    for _ in range(n):
        next(generator)


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

    powers_of_2 = closures.make_generator(lambda n: 2 ** n)

    for _ in range(10):
        print(next(powers_of_2))

    fib_gen = closures.make_generator(closures.fibonacci)

    for _ in range(10):
        print(next(fib_gen))

    fib_gen_memo = closures.make_generator_mem(closures.fibonacci)

    generate_fibs_up_to(35, fib_gen_memo())
    generate_fibs_up_to(35, fib_gen_memo())

    ducks = [Duck("John", 1, ["Carrot", "Bread"]), Duck("Tom", 4, ["Pea"])]

    kill_ducks(ducks)

