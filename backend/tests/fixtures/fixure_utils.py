import logging
import random
from dataclasses import field
from typing import Callable

from faker import Faker
from faker_biology.mol_biol import Enzyme

from app.utils import get_random_integer

logging.getLogger("faker").setLevel(logging.ERROR)
fake = Faker()
fake.add_provider(Enzyme)


def fake_user_id():
    return get_random_integer()


def fake_password(secure=True):
    if secure:
        return fake.password(length=25, special_chars=True, upper_case=True, digits=True)
    else:
        return fake.password(length=7, special_chars=False, upper_case=False, digits=False)


def fixture_field(factory_method: Callable):
    return field(default_factory=factory_method)
