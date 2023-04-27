import labs.lab7.src.password_generator as password_generator
import pytest


class TestPasswordGenerator:

    @pytest.fixture()
    def generator(self):
        return password_generator.PasswordGenerator(10, count=5)

    def test_iterator_with_next(self, generator):
        next(generator)
        next(generator)
        next(generator)
        next(generator)
        next(generator)
        with pytest.raises(StopIteration):
            next(generator)

    def test_iterator_with_for(self, generator):
        i = 0
        for psswd in generator:
            i += 1
        assert i == 5
