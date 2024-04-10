import uuid

from fixtures.fixture_utils import fake


def get_new_uuid():
    """returns a new uuid"""
    return str(uuid.uuid4())


class MockGoogleMapsClient:
    def geocode(self, address: dict = None):
        lat, lng = 0, 0

        if address:
            # Use address hash value to create a seed for the fake lat/long
            # so that the same address always returns the same lat/long
            fake.seed_instance(hash(address))
            lat, lng = fake.latlng()

        return [{"geometry": {"location": {"lat": lat, "lng": lng}}}]


def ordinal(n: int):
    """
    Convert an integer into its ordinal representation.
    """
    suffix = "th" if (11 <= (n % 100) <= 13) else ["th", "st", "nd", "rd", "th"][min(n % 10, 4)]
    return str(n) + suffix
