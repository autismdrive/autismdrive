from dataclasses import dataclass, field
from .fixure_utils import fake
from .resource import MockResource


@dataclass
class MockLocation(MockResource):
    """A Location with for testing with just the required fields filled in."""

    type: str = field(default_factory=lambda: "location")
    primary_contact: str = field(default_factory=lambda: fake.name())
    street_address1: str = field(default_factory=lambda: fake.street_address())
    street_address2: str = field(default_factory=lambda: "")
    city: str = field(default_factory=lambda: fake.city())
    state: str = field(default_factory=lambda: fake.country_code())
    zip: str = field(default_factory=lambda: fake.postcode())
    email: str = field(default_factory=lambda: fake.email())


@dataclass
class MockLocationWithLatLong(MockLocation):
    """A Location with for testing with fake latitude & longitude."""

    latitude: float = field(default_factory=lambda: fake.latitude())
    longitude: float = field(default_factory=lambda: fake.longitude())
