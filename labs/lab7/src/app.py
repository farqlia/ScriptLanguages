import log_decorator
import typing
import logging
import password_generator
import closures


@log_decorator.log(logging.DEBUG)
class Duck:

    def __init__(self, name: str, age: int, fav_food: typing.List[str]):
        self.name = name
        self.age = age
        self.fav_food = fav_food

    def quack(self):
        return "quack"


@log_decorator.log(logging.WARNING)
def kill_ducks(ducks: typing.List[Duck], n_tortures=999):
    for duck in ducks:
        for _ in range(n_tortures):
            duck.quack()

    return len(ducks)


if __name__ == "__main__":

    fib_gen = closures.make_generator(closures.fibonacci)
    for _ in range(10):
        print(fib_gen())

    # TODO : implement with memoization
    # fib_gen_memo =

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

    ducks = [Duck("John", 1, ["Carrot", "Bread"]), Duck("Tom", 4, ["Pea"])]

    kill_ducks(ducks)

