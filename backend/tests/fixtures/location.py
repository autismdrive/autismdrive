import math
import random
from dataclasses import dataclass, field

from .fixture_utils import fake
from .resource import MockResource


def fake_coords(
    latitude: float = 37.926868,
    longitude: float = -78.024902,
    min_radius_miles: float = 70,
    max_radius_miles: float = 70,
) -> dict[str, float]:
    """
    Returns fake coordinates further than the given minimum radius (in miles)
    but closer than the given maximum radius of the given center coordinates.
    """
    # Convert to radians
    lat_radians = math.radians(latitude)
    lon_radians = math.radians(longitude)

    # Earth radius in miles
    earth_radius = 3958.8

    # Random distance and bearing
    radius = random.uniform(min_radius_miles, max_radius_miles)
    bearing = math.radians(random.uniform(0, 360))  # Convert to radians

    # Angular distance
    angular_distance = radius / earth_radius

    # Destination point calculations
    dest_lat = math.asin(
        math.sin(lat_radians) * math.cos(angular_distance)
        + math.cos(lat_radians) * math.sin(angular_distance) * math.cos(bearing)
    )

    dest_lon = lon_radians + math.atan2(
        math.sin(bearing) * math.sin(angular_distance) * math.cos(lat_radians),
        math.cos(angular_distance) - math.sin(lat_radians) * math.sin(dest_lat),
    )

    # Convert back to degrees
    return {
        "latitude": math.degrees(dest_lat),
        "longitude": math.degrees(dest_lon),
    }


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

    latitude: float = field(default_factory=lambda: fake_coords()["latitude"])
    longitude: float = field(default_factory=lambda: fake_coords()["longitude"])
