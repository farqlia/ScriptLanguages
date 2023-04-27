import functools
import sys
from functools import cache

# We have four types of namespaces
# 1. built-in
# 2. global
# 3. enclosing
# 4. local


def make_generator(func):
    n = 0

    def inner():
        nonlocal n
        n += 1
        return func(n)

    return inner


def decorate_with_cache(func):

    @functools.wraps(func)
    @cache
    def cached_func(n):
        return func(n)

    wrapper_with_cache = functools.update_wrapper(cached_func, func)
    return wrapper_with_cache
    # return cached_func


def make_generator_mem(func):
    n = 0

    func_with_cache = decorate_with_cache(func)

    def inner():
        nonlocal n
        n += 1
        return func_with_cache(n)

    return inner


def make_generator_mem_inner_annot(func):
    n = 0
    @cache
    def inner(x):
        nonlocal n
        n += 1
        return func(n)

    return inner


def fibonacci(n):
    if n == 0:
        return 0
    elif n == 1:
        return 1
    else:
        return fibonacci(n - 1) + fibonacci(n - 2)


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