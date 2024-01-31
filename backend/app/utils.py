import re


def pascal_case_it(name: str) -> str:
    """Returns the given string as PascalCase string"""
    snake_cased_str = snake_case_it(name)
    first, *rest = snake_cased_str.split("_")
    return first.capitalize() + "".join(word.capitalize() for word in rest)


def snake_case_it(name: str) -> str:
    """Returns the given string as snake_case string"""
    return re.sub("([a-z0-9])([A-Z])", r"\1_\2", name).lower()
