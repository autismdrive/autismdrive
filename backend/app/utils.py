def camel_case_it(name):
    first, *rest = name.split("_")
    return first.capitalize() + "".join(word.capitalize() for word in rest)


def snake_case_it(name):
    import re

    s1 = re.sub("(.)([A-Z][a-z]+)", r"\1_\2", name)
    return re.sub("([a-z0-9])([A-Z])", r"\1_\2", s1).lower()
