import datetime
from dataclasses import dataclass, field

from app.models import User
from fixtures.location import MockLocation, MockLocationWithLatLong
from .fixure_utils import fake


@dataclass
class MockEvent(MockLocation):
    """An Event with for testing with just the required fields filled in."""

    date: datetime.datetime = field(default_factory=lambda: fake.future_datetime())
    time: str = field(default_factory=lambda: fake.time_object().strftime("%H:%M"))
    ticket_cost: str = field(default_factory=lambda: fake.pricetag())


@dataclass
class MockEventWithAllTheThings(MockLocationWithLatLong, MockEvent):
    """An Event with for testing with fake values for all most fields."""

    # # Inherited from MockResource
    # type
    # title
    # description
    # phone
    # website
    # is_draft
    # organization_name
    # is_uva_education_content
    #
    # # Inherited from MockLocation
    # primary_contact
    # street_address1
    # street_address2
    # city
    # state
    # zip
    # email
    # latitude
    # longitude
    #
    # # Inherited from MockEvent
    # date
    # time
    # ticket_cost

    post_survey_link: str = field(default_factory=lambda: fake.url())
    webinar_link: str = field(default_factory=lambda: fake.url())
    includes_registration = (True,)
    max_users: int = 35
    registered_users: list[User] = field(default_factory=list)
    post_event_description: str = field(default_factory=lambda: fake.paragraph())
