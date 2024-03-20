import re
from random import randint


class RandomInts(object):
    """A singleton class to hold the set of previously-generated random integers"""

    # Initialize RandomInts as a Singleton
    _instance: "RandomInts" = None
    _ints = set()

    def __init__(self):
        RandomInts.instance()

    @classmethod
    def instance(cls) -> "RandomInts":
        if cls._instance is None:
            cls._instance = cls.__new__(cls)

        return cls._instance

    def new_int(self) -> int:
        """Returns a random 32-bit (4-byte) signed integer that is not already in the set, ensuring uniqueness"""
        min_ = 100

        # max value for a 32-bit (4-byte) signed integer
        # https://www.postgresql.org/docs/current/datatype-numeric.html
        max_ = 2147483647

        while True:
            int_ = randint(min_, max_)
            if int_ not in self._instance._ints:
                self._instance._ints.add(int_)
                return int_


def get_random_integer() -> int:
    return RandomInts().new_int()


def pascal_case_it(name: str) -> str:
    """Returns the given string as PascalCase string"""
    snake_cased_str = snake_case_it(name)
    first, *rest = snake_cased_str.split("_")
    return first.capitalize() + "".join(word.capitalize() for word in rest)


def snake_case_it(name: str) -> str:
    """Returns the given string as snake_case string"""
    return re.sub("([a-z0-9])([A-Z])", r"\1_\2", name).lower()
