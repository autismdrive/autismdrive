import logging
from dataclasses import field
from typing import Callable

from faker import Faker
from faker_biology.mol_biol import Enzyme

logging.getLogger("faker").setLevel(logging.ERROR)
fake = Faker()
fake.add_provider(Enzyme)


def fixture_field(factory_method: Callable):
    return field(default_factory=factory_method)
