import logging
from dataclasses import field
from typing import Callable

from faker import Faker

logging.getLogger("faker").setLevel(logging.ERROR)
fake = Faker()


def fixture_field(factory_method: Callable):
    return field(default_factory=factory_method)
