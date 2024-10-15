from dataclasses import dataclass, field
from random import choice

from .fixure_utils import fake


@dataclass()
class MockResource:
    """A Resource for testing with just the required fields filled in."""

    type: str = field(default_factory=lambda: "resource")
    title: str = field(default_factory=lambda: fake.catch_phrase())
    description: str = field(default_factory=lambda: fake.paragraph())
    phone: str = field(default_factory=lambda: fake.phone_number())
    website: str = field(default_factory=lambda: fake.profile()["website"][0])
    is_draft: bool = field(default_factory=lambda: choice([True, False]))
    organization_name: str = field(default_factory=lambda: fake.company())
    is_uva_education_content: bool = field(default_factory=lambda: choice([True, False]))
