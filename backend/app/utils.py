import re

from sqlalchemy.orm import InstrumentedAttribute
from sqlalchemy.orm.collections import InstrumentedList


def pascal_case_it(name: str) -> str:
    """Returns the given string as PascalCase string"""
    snake_cased_str = snake_case_it(name)
    first, *rest = snake_cased_str.split("_")
    return first.capitalize() + "".join(word.capitalize() for word in rest)


def snake_case_it(name: str) -> str:
    """Returns the given string as snake_case string"""
    return re.sub("([a-z0-9])([A-Z])", r"\1_\2", name).lower()


def patch_dict(a: dict, b: dict, path: list = None):
    """
    Overrides the values of dict a with the values of dict b, recursively.

    a is modified in place. b can be a subset of a, or can contain new keys not in a.
    """
    if path is None:
        path = []

    for key in b:
        if key in a:
            if isinstance(a[key], dict) and isinstance(b[key], dict):
                patch_dict(a[key], b[key], path + [str(key)])
            else:
                a[key] = b[key]
        else:
            a[key] = b[key]

    return a


class Singleton(object):
    _instance = None

    def __init__(self):
        raise Exception("call instance()")

    @classmethod
    def instance(cls):
        if cls._instance is None:
            cls._instance = cls.__new__(cls)
            # more init operation here
        return cls._instance
