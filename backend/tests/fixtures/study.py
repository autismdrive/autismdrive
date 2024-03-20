from dataclasses import dataclass, field

from app.enums import Status
from .fixure_utils import fake


@dataclass
class MockStudy:
    title: str = field(default_factory=lambda: fake.catch_phrase())
    benefit_description: str = field(default_factory=lambda: fake.sentence())
    organization_name: str = field(default_factory=lambda: fake.company())
    coordinator_email: str = field(default_factory=lambda: fake.email())
    description: str = field(default_factory=lambda: fake.paragraph())
    participant_description: str = field(default_factory=lambda: fake.sentence())
    status: str = field(default_factory=lambda: fake.random_element(Status.options()))


@dataclass
class MockStudyWithMoreFields(MockStudy):
    short_title: str = field(default_factory=lambda: fake.sentence())
    short_description: str = field(default_factory=lambda: fake.sentence())
    image_url: str = field(default_factory=lambda: fake.image_url())
