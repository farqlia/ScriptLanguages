import functools
import sys
from functools import cache

# We have four types of namespaces
# 1. built-in
# 2. global
# 3. enclosing
# 4. local


# Domknięcie polega na odniesieniu się w funkcji wewnętrznej
# do zmiennych z funkcji zewnętrznej i w ten sposób nawet po
# zakończeniu wywołania tej funkcji zmienne są dostępne
def make_generator(func):

    def inner():
        n = 1
        while True:
            yield func(n)
            n += 1

    return inner()


def fibonacci(n):
    return n if n <= 1 else fibonacci(n - 1) + fibonacci(n - 2)


# to nie jest generator tak naprawdę
def make_generator_mem(func):

    cached_func = functools.cache(func)

    def gen_with_memo():
        return make_generator(cached_func)

    return gen_with_memo


def decorate_with_cache(func):

    cached_func = functools.cache(func)
    return cached_func
    # return cached_func


def make_generator_mem_inner_annot(func):
    n = 0
    @cache
    def inner(x):
        nonlocal n
        n += 1
        return func(n)

    return inner



y = 3


def test_closure():
    z = 4
    def global_f():
        def inner(x):
            # nonlocal y
            nonlocal z
            z = 6
            y = 5
            return x + y + z
        return inner
    print(global_f()(4))