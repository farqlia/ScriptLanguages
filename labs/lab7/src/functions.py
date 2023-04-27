import re
import typing
import functools
NON_WORDS = re.compile("\W+")


def acronym(strings):
    # return "" if not strings else strings[0][0].upper() + acronym(strings[1:])
    return functools.reduce(lambda acc, s: acc + s[0].upper(), strings, "")


def median(nums):
    nums = sorted(nums)
    n_half = len(nums) // 2
    return nums[n_half] if len(nums) % 2 == 1 else sum(nums[n_half - 1: n_half + 1]) / 2


def sqrt_newton(num, epsilon):

    def loop(x):
        root = 0.5 * (x + (num / x))
        return root if abs(root ** 2 - num) < epsilon else loop(root)
    return loop(1)


def make_alpha_dict(string: str):
    strings = re.split(NON_WORDS, string)
    letters = set(re.sub(NON_WORDS, "", string))
    alpha_dict = {k: list(filter(lambda s: k in s, strings)) for k in letters}
    return alpha_dict


def flatten(sequence):
    return [sequence] if not isinstance(sequence, typing.Iterable) else \
        [elem for compound in sequence for elem in flatten(compound)]



