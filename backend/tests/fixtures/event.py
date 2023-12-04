import datetime
from dataclasses import dataclass, field

from fixtures.location import MockLocation, MockLocationWithLatLong
from .fixure_utils import fake


@dataclass
class MockEvent(MockLocation):
    """An Event with for testing with just the required fields filled in."""

    date: datetime.datetime = field(default_factory=lambda: fake.future_datetime())
    time: str = field(default_factory=lambda: fake.time_object().strftime("%H:%M"))
    ticket_cost: str = field(default_factory=lambda: fake.pricetag())


@dataclass
class MockEventWithLatLong(MockLocationWithLatLong, MockEvent):
    """An Event with for testing with fake latitude & longitude."""
