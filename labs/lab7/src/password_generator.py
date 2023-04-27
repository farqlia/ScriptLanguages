import string
import sys
import random


class PasswordGenerator:

    def __init__(self, length, charset=string.ascii_letters + string.digits, count=sys.maxsize, seed=42):
        self.length = length
        self.charset = charset
        self.count = count
        self.n_generated = 0
        random.seed(seed)

    def generate_password(self):
        return "".join(random.choices(self.charset, k=self.length))

    def __iter__(self):
        self.n_generated = 0
        return self

    def __next__(self):
        if self.n_generated == self.count:
            raise StopIteration
        self.n_generated += 1
        return self.generate_password()
