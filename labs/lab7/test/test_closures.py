import functools
import sys

import labs.lab7.src.closures as closures
import pytest
from functools import cache


def test_function_inners():
    print(dir(closures.fibonacci))
    print(closures.fibonacci.__qualname__)
    print(closures.fibonacci.__code__)


@pytest.mark.parametrize("n,expected",
                         [(7, [1, 1, 2, 3, 5, 8, 13])])
def test_generate_fibonacci_nums(n, expected):
    gen = closures.make_generator(closures.fibonacci)
    fibs = []
    for i in range(7):
        fibs.append(next(gen))

    assert fibs == expected


@pytest.mark.parametrize("func,n,expected",
                         [
                             (lambda x: x, 5, [1, 2, 3, 4, 5]),
                             (lambda q: 2 ** (q - 1), 5, [1, 2, 4, 8, 16]),
                             (lambda n: n ** 2, 5, [1, 4, 9, 16, 25])
                         ])
def test_generate_sequence(func, n, expected):
    gen = closures.make_generator(func)
    sequence = []
    for i in range(n):
        sequence.append(next(gen))

    assert sequence == expected


def test_generate_fibonacci_nums_with_cache():
    sys.setrecursionlimit(100)
    gen_wrapper = closures.make_generator_mem(closures.fibonacci)
    gen = gen_wrapper()
    fibs = []

    for i in range(20):
        fibs.append(gen())


    gen = gen_wrapper()
    for i in range(20):
        gen()

    print(dir(gen))
    print(gen.__closure__[0])

@cache
def fibonacci(n):
    if n <= 1:
        return n
    return fibonacci(n - 1) + fibonacci(n - 2)


def fibonacci_without_cache(n):
    if n <= 1:
        return n
    return fibonacci_without_cache(n - 1) + fibonacci_without_cache(n - 2)


def generate_fibs():
    n = 0
    @cache
    def fibonacci(n):
        if n <= 1:
            return n
        return fibonacci(n - 1) + fibonacci(n - 2)

    def inner_fib():
        nonlocal n
        n += 1
        return fibonacci(n)

    return inner_fib

def test_how_caching_works4():
    sys.setrecursionlimit(100)
    gen = generate_fibs()
    for i in range(102):
        print(gen(), end=", ")
    print(dir(gen))
    print(gen.__closure__)
    # print(gen.cache_info())
    # print(gen.cache_parameters)

def test_how_caching_works_2():
    # sys.setrecursionlimit(100)
    cached_fib = closures.decorate_with_cache(fibonacci_without_cache)
    cached_with_annot = fibonacci

    # gen = closures.make_generator_mem(fibonacci_without_cache)
    for i in range(20):
        num = cached_with_annot(i)
        num2 = cached_fib(i)
        print(num, num2, end=",")
    # print(dir(gen))
    # print(dir(closures.make_generator_mem))
    print(cached_fib.cache_info())
    print(cached_with_annot.cache_info())
    # print(closures.make_generator_mem.cache_info())


def test_how_caching_works():
    sys.setrecursionlimit(100)
    for i in range(102):
        print(fibonacci(i), end=",")
    print(fibonacci.__annotations__)
    print(fibonacci.__wrapped__)
    print(dir(fibonacci))
    print(fibonacci.cache_info())
    print(fibonacci.cache_parameters)


def test_how_caching_works3():
    gen = closures.make_generator_mem_inner_annot(closures.fibonacci)
    for i in range(102):
        gen(1)
    print(dir(gen))
    print(dir(closures.make_generator_mem_inner_annot))
    print(gen.cache_info())
    print(gen.cache_parameters())
    print(functools.cached_property(gen))


def test_how_caching_works_4():
    cached_fib = functools.cache(fibonacci_without_cache)
    for i in range(102):
        print(cached_fib(i), end=",")