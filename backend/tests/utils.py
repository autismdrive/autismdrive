import uuid

from fixtures.fixure_utils import fake


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
